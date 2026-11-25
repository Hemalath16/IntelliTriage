
import math
import uuid

from flask import Blueprint, request, jsonify

from services.auth_service import verify_user
from config.supabase_client import get_authenticated_client


nurse_bp = Blueprint("nurse", __name__)


# --------------------------------------------------
# HELPER: Verify user role and create authenticated client
# --------------------------------------------------

def get_user_client(allowed_roles):

    user, error = verify_user()

    if error:
        return None, None, (jsonify({"error": error}), 401)

    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ", 1)[1]
    client = get_authenticated_client(token)

    try:
        role_result = (
            client.table("user_roles")
            .select("role")
            .eq("user_id", user.id)
            .single()
            .execute()
        )

        role = role_result.data["role"]

        if role not in allowed_roles:
            return None, None, (
                jsonify({"error": "You are not authorized to perform this action"}),
                403
            )

    except Exception:
        return None, None, (
            jsonify({"error": "Unable to verify user role"}),
            403
        )

    return user, client, None


# --------------------------------------------------
# GET: View patient records
# --------------------------------------------------

@nurse_bp.route("/api/nurse/patients", methods=["GET"])
def get_patients():

    user, client, error_response = get_user_client(
        ["nurse", "doctor", "receptionist"]
    )

    if error_response:
        return error_response

    try:
        result = (
            client.table("patients")
            .select(
                "id, patient_code, first_name, last_name, "
                "date_of_birth, gender, phone, email, address, created_at"
            )
            .order("created_at", desc=True)
            .execute()
        )

        return jsonify({
            "message": "Patients retrieved successfully",
            "patients": result.data
        }), 200

    except Exception:
        return jsonify({
            "error": "Unable to retrieve patients"
        }), 500


# --------------------------------------------------
# POST: Create a new patient visit
# --------------------------------------------------

@nurse_bp.route("/api/nurse/visits", methods=["POST"])
def create_visit():

    user, client, error_response = get_user_client(
        ["nurse", "doctor"]
    )

    if error_response:
        return error_response

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Valid JSON request data is required"
        }), 400

    patient_id = data.get("patient_id")
    chief_complaint = data.get("chief_complaint")

    if not patient_id:
        return jsonify({"error": "Patient ID is required"}), 400

    try:
        patient_id = str(uuid.UUID(patient_id))
    except (ValueError, TypeError, AttributeError):
        return jsonify({"error": "Invalid patient ID"}), 400

    if not isinstance(chief_complaint, str) or not chief_complaint.strip():
        return jsonify({
            "error": "Valid chief complaint is required"
        }), 400

    chief_complaint = chief_complaint.strip()

    if len(chief_complaint) > 1000:
        return jsonify({"error": "Chief complaint is too long"}), 400

    visit_type = data.get("visit_type")

    if visit_type is not None:
        if not isinstance(visit_type, str) or not visit_type.strip():
            return jsonify({"error": "Invalid visit type"}), 400
        visit_type = visit_type.strip()

    try:
        visit_data = {
            "patient_id": patient_id,
            "chief_complaint": chief_complaint,
            "visit_type": visit_type,
            "recorded_by": user.id
        }

        result = (
            client.table("visits")
            .insert(visit_data)
            .execute()
        )

        return jsonify({
            "message": "Visit created successfully",
            "visit": result.data
        }), 201

    except Exception:
        return jsonify({
            "error": "Visit creation failed"
        }), 500


# --------------------------------------------------
# POST: Record vital signs
# --------------------------------------------------

@nurse_bp.route(
    "/api/nurse/visits/<visit_id>/vitals",
    methods=["POST"]
)
def record_vital_signs(visit_id):

    user, client, error_response = get_user_client(
        ["nurse", "doctor"]
    )

    if error_response:
        return error_response

    try:
        visit_id = str(uuid.UUID(visit_id))
    except (ValueError, TypeError, AttributeError):
        return jsonify({"error": "Invalid visit ID"}), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON data is required"}), 400

    fields = [
        "temperature",
        "heart_rate",
        "respiratory_rate",
        "systolic_bp",
        "diastolic_bp",
        "oxygen_saturation"
    ]

    if not any(data.get(field) is not None for field in fields):
        return jsonify({
            "error": "At least one vital sign is required"
        }), 400

    values = {}

    for field in fields:

        value = data.get(field)

        if value is None:
            values[field] = None
            continue

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return jsonify({
                "error": f"{field} must be numeric"
            }), 400

        if not math.isfinite(value):
            return jsonify({
                "error": f"{field} must be a finite number"
            }), 400

        if field in [
            "heart_rate",
            "respiratory_rate",
            "systolic_bp",
            "diastolic_bp"
        ]:
            if not isinstance(value, int) or value <= 0:
                return jsonify({
                    "error": f"{field} must be a positive integer"
                }), 400

        if field == "temperature" and not -50 <= value <= 100:
            return jsonify({
                "error": "Invalid temperature value"
            }), 400

        if field == "oxygen_saturation" and not 0 <= value <= 100:
            return jsonify({
                "error": "oxygen_saturation must be between 0 and 100"
            }), 400

        values[field] = value

    values["visit_id"] = visit_id
    values["recorded_by"] = user.id

    try:
        result = (
            client.table("vital_signs")
            .insert(values)
            .execute()
        )

        return jsonify({
            "message": "Vital signs recorded successfully",
            "vital_signs": result.data
        }), 201

    except Exception:
        return jsonify({
            "error": "Failed to record vital signs"
        }), 500


# --------------------------------------------------
# GET: Retrieve vital signs for a visit
# --------------------------------------------------

@nurse_bp.route(
    "/api/nurse/visits/<visit_id>/vitals",
    methods=["GET"]
)
def get_vital_signs(visit_id):

    user, client, error_response = get_user_client(
        ["nurse", "doctor"]
    )

    if error_response:
        return error_response

    try:
        visit_id = str(uuid.UUID(visit_id))
    except (ValueError, TypeError, AttributeError):
        return jsonify({"error": "Invalid visit ID"}), 400

    try:
        visit_result = (
            client.table("visits")
            .select("id")
            .eq("id", visit_id)
            .limit(1)
            .execute()
        )

        if not visit_result.data:
            return jsonify({"error": "Visit not found"}), 404

        result = (
            client.table("vital_signs")
            .select("*")
            .eq("visit_id", visit_id)
            .order("recorded_at", desc=True)
            .execute()
        )

        return jsonify({
            "message": "Vital signs retrieved successfully",
            "vital_signs": result.data
        }), 200

    except Exception:
        return jsonify({
            "error": "Failed to retrieve vital signs"
        }), 500

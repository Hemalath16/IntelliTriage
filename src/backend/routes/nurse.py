
import uuid

from flask import Blueprint, request, jsonify

from services.auth_service import verify_user
from config.supabase_client import get_authenticated_client


nurse_bp = Blueprint("nurse", __name__)


# GET: View patient records
@nurse_bp.route("/api/nurse/patients", methods=["GET"])
def get_patients():

    # Step 1: Verify logged-in user
    user, error = verify_user()

    if error:
        return jsonify({"error": error}), 401

    # Step 2: Get authenticated client
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ", 1)[1]
    client = get_authenticated_client(token)

    # Step 3: Check user role
    try:
        role_result = (
            client.table("user_roles")
            .select("role")
            .eq("user_id", user.id)
            .single()
            .execute()
        )

        role = role_result.data["role"]

        if role not in ["nurse", "doctor", "receptionist"]:
            return jsonify({
                "error": "You are not authorized to view patients"
            }), 403

    except Exception:
        return jsonify({
            "error": "Unable to verify user role"
        }), 403

    # Step 4: Fetch patients
    try:
        result = (
            client.table("patients")
            .select("*")
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


# POST: Create a new patient visit
@nurse_bp.route("/api/nurse/visits", methods=["POST"])
def create_visit():

    # Step 1: Verify logged-in user
    user, error = verify_user()

    if error:
        return jsonify({"error": error}), 401

    # Step 2: Get authenticated client
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ", 1)[1]
    client = get_authenticated_client(token)

    # Step 3: Verify nurse or doctor role
    try:
        role_result = (
            client.table("user_roles")
            .select("role")
            .eq("user_id", user.id)
            .single()
            .execute()
        )

        role = role_result.data["role"]

        if role not in ["nurse", "doctor"]:
            return jsonify({
                "error": "Only nurses and doctors can create visits"
            }), 403

    except Exception:
        return jsonify({
            "error": "Unable to verify user role"
        }), 403

    # Step 4: Validate request data
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Valid JSON request data is required"
        }), 400

    patient_id = data.get("patient_id")
    chief_complaint = data.get("chief_complaint")

    if not patient_id:
        return jsonify({
            "error": "Patient ID is required"
        }), 400

    try:
        patient_id = str(uuid.UUID(patient_id))
    except (ValueError, TypeError, AttributeError):
        return jsonify({
            "error": "Invalid patient ID"
        }), 400

    if not isinstance(chief_complaint, str) or not chief_complaint.strip():
        return jsonify({
            "error": "Valid chief complaint is required"
        }), 400

    chief_complaint = chief_complaint.strip()

    if len(chief_complaint) > 1000:
        return jsonify({
            "error": "Chief complaint is too long"
        }), 400

    # Step 5: Create visit
    try:
        visit_data = {
            "patient_id": patient_id,
            "chief_complaint": chief_complaint,
            "visit_type": data.get("visit_type"),
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

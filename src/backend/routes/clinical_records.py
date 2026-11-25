
from flask import Blueprint, request, jsonify
from uuid import UUID

from services.auth_service import verify_user
from config.supabase_client import get_authenticated_client


clinical_records_bp = Blueprint(
    "clinical_records",
    __name__
)


# Authenticate user and verify role
def get_clinical_client():

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

        if role not in ["nurse", "doctor"]:
            return None, None, (
                jsonify({
                    "error": "Only nurses and doctors can access clinical records"
                }),
                403
            )

    except Exception as error:
        print("ROLE VERIFICATION ERROR:", repr(error))

        return None, None, (
            jsonify({"error": "Unable to verify user role"}),
            403
        )

    return client, user, None


# Validate UUID
def valid_uuid(value):

    try:
        UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False


# 1. Record patient symptoms
@clinical_records_bp.route(
    "/api/clinical/symptoms",
    methods=["POST"]
)
def record_symptoms():

    client, user, error_response = get_clinical_client()

    if error_response:
        return error_response

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request data is required"}), 400

    visit_id = data.get("visit_id")
    symptom_name = data.get("symptom_name")

    if not visit_id or not symptom_name:
        return jsonify({
            "error": "Visit ID and symptom name are required"
        }), 400

    if not valid_uuid(visit_id):
        return jsonify({"error": "Invalid visit ID"}), 400

    if not isinstance(symptom_name, str) or not symptom_name.strip():
        return jsonify({"error": "Invalid symptom name"}), 400

    symptom_data = {
        "visit_id": visit_id,
        "symptom_name": symptom_name.strip(),
        "description": data.get("description"),
        "duration": data.get("duration"),
        "severity": data.get("severity"),
        "onset_date": data.get("onset_date"),
        "recorded_by": user.id
    }

    try:
        result = (
            client.table("patient_symptoms")
            .insert(symptom_data)
            .execute()
        )

        return jsonify({
            "message": "Patient symptoms recorded successfully",
            "symptom": result.data
        }), 201

    except Exception as error:
        print("SYMPTOM INSERT ERROR:", repr(error))

        return jsonify({
            "error": "Unable to record patient symptoms"
        }), 500


# 2. View symptoms for a visit
@clinical_records_bp.route(
    "/api/clinical/visits/<visit_id>/symptoms",
    methods=["GET"]
)
def get_symptoms(visit_id):

    client, user, error_response = get_clinical_client()

    if error_response:
        return error_response

    if not valid_uuid(visit_id):
        return jsonify({"error": "Invalid visit ID"}), 400

    try:
        result = (
            client.table("patient_symptoms")
            .select("*")
            .eq("visit_id", visit_id)
            .order("created_at", desc=True)
            .execute()
        )

        return jsonify({
            "symptoms": result.data
        }), 200

    except Exception as error:
        print("SYMPTOM RETRIEVAL ERROR:", repr(error))

        return jsonify({
            "error": "Unable to retrieve patient symptoms"
        }), 500


# 3. Record medical history
@clinical_records_bp.route(
    "/api/clinical/medical-history",
    methods=["POST"]
)
def record_medical_history():

    client, user, error_response = get_clinical_client()

    if error_response:
        return error_response

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request data is required"}), 400

    patient_id = data.get("patient_id")
    condition_name = data.get("condition_name")

    if not patient_id or not condition_name:
        return jsonify({
            "error": "Patient ID and condition name are required"
        }), 400

    if not valid_uuid(patient_id):
        return jsonify({"error": "Invalid patient ID"}), 400

    if not isinstance(condition_name, str) or not condition_name.strip():
        return jsonify({"error": "Invalid condition name"}), 400

    history_data = {
        "patient_id": patient_id,
        "condition_name": condition_name.strip(),
        "description": data.get("description"),
        "diagnosed_date": data.get("diagnosed_date"),
        "status": data.get("status"),
        "recorded_by": user.id
    }

    try:
        result = (
            client.table("medical_history")
            .insert(history_data)
            .execute()
        )

        return jsonify({
            "message": "Medical history recorded successfully",
            "medical_history": result.data
        }), 201

    except Exception as error:
        print("MEDICAL HISTORY INSERT ERROR:", repr(error))

        return jsonify({
            "error": "Unable to record medical history"
        }), 500


# 4. View medical history for a patient
@clinical_records_bp.route(
    "/api/clinical/patients/<patient_id>/medical-history",
    methods=["GET"]
)
def get_medical_history(patient_id):

    client, user, error_response = get_clinical_client()

    if error_response:
        return error_response

    if not valid_uuid(patient_id):
        return jsonify({"error": "Invalid patient ID"}), 400

    try:
        result = (
            client.table("medical_history")
            .select("*")
            .eq("patient_id", patient_id)
            .order("created_at", desc=True)
            .execute()
        )

        return jsonify({
            "medical_history": result.data
        }), 200

    except Exception as error:
        print("MEDICAL HISTORY RETRIEVAL ERROR:", repr(error))

        return jsonify({
            "error": "Unable to retrieve medical history"
        }), 500

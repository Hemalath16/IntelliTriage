from flask import Blueprint, request, jsonify
from services.supabase_service import get_supabase_client

patients_bp = Blueprint("patients", __name__)

@patients_bp.route("/api/patients", methods=["POST"])
def register_patient():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Patient information is required"}), 400

    required_fields = ["first_name"]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    supabase = get_supabase_client()

    try:
        code_result = supabase.rpc(
            "generate_patient_code"
        ).execute()

        patient_code = code_result.data

        patient_data = {
            "patient_code": patient_code,
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "date_of_birth": data.get("date_of_birth"),
            "gender": data.get("gender"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "address": data.get("address")
        }

        result = supabase.table("patients").insert(
            patient_data
        ).execute()

        return jsonify({
            "message": "Patient registered successfully",
            "patient": result.data
        }), 201

    except Exception:
        return jsonify({
            "error": "Patient registration failed"
        }), 500

from flask import Blueprint, request, jsonify
from services.supabase_service import get_supabase_client
from services.auth_service import verify_user
from config.supabase_client import get_authenticated_client

patients_bp = Blueprint("patients", __name__)


@patients_bp.route("/api/patients", methods=["POST"])
def register_patient():

    # Step 1: Verify the logged-in user
    user, error = verify_user()

    if error:
        return jsonify({"error": error}), 401

    # Step 2: Create a client using the user's access token
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ", 1)[1]
    client = get_authenticated_client(token)

    # Step 3: Check the user's role
    try:
        role_result = (
            client.table("user_roles")
            .select("role")
            .eq("user_id", user.id)
            .single()
            .execute()
        )

        if role_result.data["role"] != "receptionist":
            return jsonify({
                "error": "Only receptionists can register patients"
            }), 403

    except Exception:
        return jsonify({
            "error": "Unable to verify user role"
        }), 403

    # Step 4: Validate patient information
    data = request.get_json(silent=True)

    if not data or not data.get("first_name"):
        return jsonify({
            "error": "Patient first name is required"
        }), 400

    # Step 5: Generate patient code and register patient
    try:
        code_result = client.rpc(
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
            "address": data.get("address"),
            "created_by": user.id
        }

        result = client.table("patients").insert(
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

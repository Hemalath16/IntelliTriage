
from flask import Blueprint, request, jsonify

from services.staff_auth_service import register_staff
from services.auth_service import verify_user
from config.supabase_client import get_admin_client

staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/api/staff/register", methods=["POST"])
def staff_registration():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request data is required"}), 400

    result, error = register_staff(data)

    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 201


@staff_bp.route("/api/staff/pending", methods=["GET"])
def get_pending_staff():
    user, error = verify_user()

    if error:
        return jsonify({"error": error}), 401

    try:
        admin_client = get_admin_client()

        role_response = (
            admin_client.table("user_roles")
            .select("role")
            .eq("user_id", user.id)
            .maybe_single()
            .execute()
        )

        if not role_response.data or role_response.data["role"] != "admin":
            return jsonify({"error": "Administrator access required"}), 403

        response = (
            admin_client.table("staff_profiles")
            .select(
                "user_id, full_name, email, phone, role, "
                "qualification, professional_registration_number, "
                "approval_status, created_at"
            )
            .eq("approval_status", "pending")
            .order("created_at", desc=False)
            .execute()
        )

        return jsonify({"pending_staff": response.data}), 200

    except Exception as error:
        print("PENDING STAFF DEBUG:", repr(error))
        return jsonify({"error": "Unable to retrieve pending staff"}), 500


@staff_bp.route("/api/staff/<user_id>/approve", methods=["POST"])
def approve_staff(user_id):
    user, error = verify_user()

    if error:
        return jsonify({"error": error}), 401

    try:
        admin_client = get_admin_client()

        role_response = (
            admin_client.table("user_roles")
            .select("role")
            .eq("user_id", user.id)
            .maybe_single()
            .execute()
        )

        if not role_response.data or role_response.data["role"] != "admin":
            return jsonify({"error": "Administrator access required"}), 403

        response = admin_client.rpc(
            "approve_staff_profile",
            {
                "target_user_id": user_id,
                "approving_admin_id": user.id
            }
        ).execute()

        return jsonify({
            "message": "Staff approved successfully",
            "staff_code": response.data
        }), 200

    except Exception as error:
        print("STAFF APPROVAL DEBUG:", repr(error))
        return jsonify({"error": "Staff approval failed"}), 400

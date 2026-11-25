
from flask import Blueprint, request, jsonify

from services.staff_login_service import login_staff

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/login", methods=["POST"])
def staff_login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Login details are required"}), 400

    result, error = login_staff(data)

    if error:
        return jsonify({"error": error}), 401

    return jsonify(result), 200

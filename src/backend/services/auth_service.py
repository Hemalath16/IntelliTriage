from flask import request
from config.supabase_client import supabase


def verify_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None, "Authentication token is missing"

    token = auth_header.split(" ", 1)[1]

    try:
        response = supabase.auth.get_user(token)

        if not response.user:
            return None, "Invalid authentication token"

        return response.user, None

    except Exception:
        return None, "Authentication failed"
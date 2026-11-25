
from config.supabase_client import supabase, get_admin_client


def login_staff(data):
    staff_code = data.get("staff_code", "").strip().upper()
    password = data.get("password", "")

    if not staff_code or not password:
        return None, "Staff ID and password are required"

    admin_client = get_admin_client()

    try:
        # Find the staff account using its approved staff ID
        profile_response = (
            admin_client.table("staff_profiles")
            .select("user_id, staff_code, full_name, role, approval_status")
            .eq("staff_code", staff_code)
            .maybe_single()
            .execute()
        )

        profile = profile_response.data

        if not profile:
            return None, "Invalid Staff ID or password"

        if profile["approval_status"] != "approved":
            return None, "Your account is awaiting administrator approval"

        # Authenticate using Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": (
                admin_client.table("staff_profiles")
                .select("email")
                .eq("user_id", profile["user_id"])
                .single()
                .execute()
                .data["email"]
            ),
            "password": password
        })

        if not auth_response.user or not auth_response.session:
            return None, "Invalid Staff ID or password"

        return {
            "message": "Login successful",
            "staff": {
                "user_id": profile["user_id"],
                "staff_code": profile["staff_code"],
                "full_name": profile["full_name"],
                "role": profile["role"]
            },
            "access_token": auth_response.session.access_token,
            "refresh_token": auth_response.session.refresh_token
        }, None

    except Exception as error:
        print("STAFF LOGIN DEBUG:", repr(error))
        return None, "Login failed. Please check your credentials and try again."


from datetime import date
from config.supabase_client import get_admin_client


def register_staff(data):
    required_fields = [
        "full_name",
        "date_of_birth",
        "phone",
        "email",
        "password",
        "role"
    ]

    for field in required_fields:
        if not data.get(field):
            return None, f"{field} is required"

    role = data["role"].lower()

    if role not in ["receptionist", "nurse", "doctor"]:
        return None, "Invalid staff role"

    if len(data["password"]) < 8:
        return None, "Password must contain at least 8 characters"

    try:
        date.fromisoformat(data["date_of_birth"])
    except (ValueError, TypeError):
        return None, "Date of birth must use YYYY-MM-DD format"

    if role in ["nurse", "doctor"]:
        if not data.get("qualification"):
            return None, "Qualification is required"

        if not data.get("professional_registration_number"):
            return None, "Professional registration number is required"

    admin_client = get_admin_client()
    user_id = None

    try:
        response = admin_client.auth.admin.create_user({
            "email": data["email"].strip().lower(),
            "password": data["password"],
            "email_confirm": False
        })

        if not response.user:
            return None, "Account creation failed"

        user_id = response.user.id

        profile = {
            "user_id": user_id,
            "full_name": data["full_name"].strip(),
            "date_of_birth": data["date_of_birth"],
            "phone": data["phone"].strip(),
            "email": data["email"].strip().lower(),
            "role": role,
            "qualification": data.get("qualification"),
            "professional_registration_number": data.get(
                "professional_registration_number"
            ),
            "profile_photo_path": None,
            "approval_status": "pending"
        }

        admin_client.table("staff_profiles").insert(
            profile
        ).execute()

        return {
            "user_id": user_id,
            "approval_status": "pending",
            "message": "Registration submitted for administrator approval"
        }, None

    except Exception as error:
        print("STAFF REGISTRATION DEBUG:", repr(error))

        if user_id:
            try:
                admin_client.auth.admin.delete_user(user_id)
            except Exception as cleanup_error:
                print("AUTH CLEANUP ERROR:", repr(cleanup_error))

        return None, "Staff registration failed. Please check the details and try again."

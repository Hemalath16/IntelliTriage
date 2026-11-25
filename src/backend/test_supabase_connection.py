
from config.supabase_client import get_admin_client

try:
    admin_client = get_admin_client()

    response = (
        admin_client
        .table("user_roles")
        .select("role")
        .limit(1)
        .execute()
    )

    print("Supabase admin connection: SUCCESS")
    print("Database access: SUCCESS")

except Exception as error:
    print("Connection test failed:", error)


import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials are missing. Check your .env file.")

# Normal client for public/authenticated operations
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_authenticated_client(access_token):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.postgrest.auth(access_token)
    return client


# Server-only client for trusted administrative operations
admin_supabase = None

if SUPABASE_SERVICE_ROLE_KEY:
    admin_supabase = create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY
    )


def get_admin_client():
    if admin_supabase is None:
        raise ValueError("Supabase service-role key is not configured.")

    return admin_supabase

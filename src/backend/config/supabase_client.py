import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Read Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check whether credentials exist
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials are missing. Check your .env file.")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
def get_authenticated_client(access_token):
    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    client.postgrest.auth(access_token)

    return client
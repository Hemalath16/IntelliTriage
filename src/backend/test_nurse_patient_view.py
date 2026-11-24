from supabase import create_client
import requests
import os
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

EMAIL = input("Admin email: ")
PASSWORD = getpass("Admin password: ")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Nurse login
try:
    response = supabase.auth.sign_in_with_password({
        "email": EMAIL,
        "password": PASSWORD
    })

    access_token = response.session.access_token

    print("Admin login successful!")

except Exception as error:
    print("Login failed:", error)
    raise SystemExit

# Request patient records
result = requests.get(
    "http://127.0.0.1:5000/api/nurse/patients",
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)

print("HTTP Status:", result.status_code)
print("Response:", result.text)
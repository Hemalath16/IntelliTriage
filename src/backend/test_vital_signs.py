
from supabase import create_client
import requests
import os

from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

EMAIL = input("Nurse email: ")
PASSWORD = getpass("Nurse password: ")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Nurse login
try:
    response = supabase.auth.sign_in_with_password({
        "email": EMAIL,
        "password": PASSWORD
    })

    access_token = response.session.access_token
    print("\nNurse login successful!")

except Exception as error:
    print("Login failed:", error)
    raise SystemExit

# Enter existing test visit ID
visit_id = input("\nEnter test visit ID: ").strip()

headers = {
    "Authorization": f"Bearer {access_token}"
}

# Test POST: Record vital signs
vitals = {
    "temperature": 36.8,
    "heart_rate": 78,
    "respiratory_rate": 18,
    "systolic_bp": 120,
    "diastolic_bp": 80,
    "oxygen_saturation": 98
}

print("\nTesting POST vital signs...")

post_response = requests.post(
    f"http://127.0.0.1:5000/api/nurse/visits/{visit_id}/vitals",
    headers=headers,
    json=vitals
)

print("POST Status:", post_response.status_code)
print("POST Response:", post_response.text)

# Test GET: Retrieve vital signs
print("\nTesting GET vital signs...")

get_response = requests.get(
    f"http://127.0.0.1:5000/api/nurse/visits/{visit_id}/vitals",
    headers=headers
)

print("GET Status:", get_response.status_code)
print("GET Response:", get_response.text)

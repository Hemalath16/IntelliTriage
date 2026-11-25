
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
    print("Nurse login successful!")

except Exception as error:
    print("Login failed:", error)
    raise SystemExit

# Test patient ID
patient_id = input("Enter test patient ID: ")

visit_data = {
    "patient_id": patient_id,
    "chief_complaint": "Fictional test complaint for API testing",
    "visit_type": "General"
}

# Create visit
result = requests.post(
    "http://127.0.0.1:5000/api/nurse/visits",
    headers={
        "Authorization": f"Bearer {access_token}"
    },
    json=visit_data
)

print("HTTP Status:", result.status_code)
print("Response:", result.text)

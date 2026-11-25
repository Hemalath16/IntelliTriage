from supabase import create_client
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Enter the receptionist test account details locally
EMAIL = input("Admin email: ")

from getpass import getpass
PASSWORD = getpass("Admin password: ")

# Login to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

# Sample fictional patient
patient_data = {
    "first_name": "Test",
    "last_name": "Patient",
    "date_of_birth": "2000-05-15",
    "gender": "Other",
    "phone": "9999999999",
    "email": "testpatient@example.com",
    "address": "Test Address"
}

# Send registration request to Flask
result = requests.post(
    "http://127.0.0.1:5000/api/patients",
    headers={
        "Authorization": f"Bearer {access_token}"
    },
    json=patient_data
)

print("HTTP Status:", result.status_code)
print("Response:", result.text)
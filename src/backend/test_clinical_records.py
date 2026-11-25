import requests
from getpass import getpass
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_URL = "http://127.0.0.1:5000"


# Nurse login
email = input("Enter nurse email: ")
password = getpass("Enter nurse password: ")

try:
    login = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    token = login.session.access_token
    print("\nNurse login successful!")

except Exception as error:
    print("\nLogin failed:", error)
    exit()


headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}


# Enter existing visit ID
visit_id = input("\nEnter existing visit ID: ")


# Record fictional test symptoms
symptom_data = {
    "visit_id": visit_id,
    "symptom_name": "Fictional test headache",
    "description": "Test data only",
    "duration": "2 hours",
    "severity": "mild",
    "onset_date": "2026-11-25"
}

print("\nTesting symptom registration...")

response = requests.post(
    f"{BASE_URL}/api/clinical/symptoms",
    json=symptom_data,
    headers=headers
)

print("Status:", response.status_code)
print("Response:", response.json())


# Retrieve symptoms
print("\nTesting symptom retrieval...")

response = requests.get(
    f"{BASE_URL}/api/clinical/visits/{visit_id}/symptoms",
    headers=headers
)

print("Status:", response.status_code)
print("Response:", response.json())
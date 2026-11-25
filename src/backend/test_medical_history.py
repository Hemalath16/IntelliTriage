
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
    raise SystemExit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

patient_id = input("\nEnter existing patient ID: ")

history_data = {
    "patient_id": patient_id,
    "condition_name": "Fictional test medical history",
    "description": "Test data only",
    "diagnosed_date": "2025-06-10",
    "status": "active"
}

print("\nTesting medical history registration...")

response = requests.post(
    f"{BASE_URL}/api/clinical/medical-history",
    json=history_data,
    headers=headers
)

print("Status:", response.status_code)

try:
    print("Response:", response.json())
except ValueError:
    print("Response:", response.text)

print("\nTesting medical history retrieval...")

response = requests.get(
    f"{BASE_URL}/api/clinical/patients/{patient_id}/medical-history",
    headers=headers
)

print("Status:", response.status_code)

try:
    print("Response:", response.json())
except ValueError:
    print("Response:", response.text)

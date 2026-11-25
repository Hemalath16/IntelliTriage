
import requests
from getpass import getpass

BASE_URL = "http://127.0.0.1:5000"

email = input("Enter admin email: ")
password = getpass("Enter admin password: ")

try:
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    print("Login status:", login_response.status_code)
    print(login_response.text)

except requests.RequestException as error:
    print("Request failed:", error)

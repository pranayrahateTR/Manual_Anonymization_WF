"""
Standalone API script to update user role to Approver
Runs in a separate process - no browser interference
"""
import requests
import json
from pathlib import Path
import sys
import os
from dotenv import load_dotenv


def update_role_to_approver():
    """Update user role from Redactor to Approver via API"""

    # ========================================================================
    # CREDENTIAL MANAGEMENT - TWO APPROACHES:
    # ========================================================================

    # OLD APPROACH (JSON files) - COMMENTED OUT:
    # base_path = Path(__file__).parent
    # with open(base_path / "login.json", 'r') as f:
    #     credentials = json.load(f)
    # with open(base_path / "userrole_approver.json", 'r') as f:
    #     user_data = json.load(f)
    # - Reads credentials from JSON files
    # - Security risk: JSON files could be committed to Git
    # - Passwords visible in plain text files

    # NEW APPROACH (Environment variables) - ACTIVE:
    # Load environment variables from .env file
    load_dotenv()

    # Build credentials dictionary from environment variables
    credentials = {
        "userName": os.getenv("API_USERNAME"),
        "password": os.getenv("API_PASSWORD")
    }

    # Build user data dictionary from environment variables
    user_data = {
        "userId": int(os.getenv("USER_ID")),
        "firstName": os.getenv("USER_FIRSTNAME"),
        "lastName": os.getenv("USER_LASTNAME"),
        "emailId": os.getenv("USER_EMAIL"),
        "mappedId": "",
        "isActive": 1,
        "roleId": int(os.getenv("APPROVER_ROLE_ID")),  # 3 = Approver
        "location": os.getenv("USER_LOCATION")
    }

    # Validate credentials
    if not credentials["userName"] or not credentials["password"]:
        print("ERROR: API credentials not found in .env file!")
        print("Please ensure API_USERNAME and API_PASSWORD are set.")
        sys.exit(1)
    # ========================================================================

    print("Step 1: Logging in via API...")

    # Login to get token
    try:
        login_response = requests.post(
            "https://devtr-ocrjmtapi.sureprep.com/api/Authentication/Login",
            json=credentials,
            headers={"Content-Type": "application/json"}
        )

        if login_response.status_code == 200:
            token = login_response.json().get("token")
            print(f"Login successful, token obtained")
        else:
            print(f"Login failed with status {login_response.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"Login error: {e}")
        sys.exit(1)

    print("Step 2: Updating user role to Approver...")

    # Update role
    try:
        update_response = requests.post(
            "https://devtr-ocrjmtapi.sureprep.com/api/User/update-user",
            json=user_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        if update_response.status_code in [200, 201, 204]:
            print("User role updated successfully to Approver!")
            sys.exit(0)
        else:
            print(f"Update failed with status {update_response.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"Update error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    update_role_to_approver()

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NC_API_BASE_URL = os.getenv("NC_API_BASE_URL")
NC_API_GRANT_TYPE = os.getenv("NC_API_GRANT_TYPE")
NC_API_USER = os.getenv("NC_API_USER")
NC_API_PASSWORD = os.getenv("NC_API_PASSWORD")
NC_API_CLIENT_ID = os.getenv("NC_API_CLIENT_ID")

def get_access_token() -> str:
    """
    Retrieves an OAuth2 bearer token from NowCerts using hardcoded credentials.
    """
    url = f"{NC_API_BASE_URL}/token"
    payload = {
        "grant_type": NC_API_GRANT_TYPE,
        "username": NC_API_USER,
        "password": NC_API_PASSWORD,
        "client_id": NC_API_CLIENT_ID,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise Exception("Access token not found in response.")
        return token
    except requests.RequestException as e:
        raise Exception(f"Token retrieval failed: {e.response.json() if e.response else str(e)}")

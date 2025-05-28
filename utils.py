import requests

def get_access_token() -> str:
    """
    Retrieves an OAuth2 bearer token from NowCerts using hardcoded credentials.
    """
    url = "https://api.nowcerts.com/api/token"
    payload = {
        "grant_type": "password",
        "username": "api@api.api",
        "password": "123456Qw",
        "client_id": "ngAuthApp",
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

from google.adk.agents import Agent
from typing import Optional, Dict, List
import requests

# --- Internal Auth Function ---

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

# --- Tool Functions ---

def create_renewal_opportunity(
    created_from_renewal: bool,
    line_of_business_name: str,
    needed_by: str,
    opportunity_stage_name: str,
    current_stage_due_date: str,
    referral_source_name: str,
    referral_source_contact_name: str,
    win_probability: str,
    agency_commission: float,
    assigned_to: List[str],
    description: str,
    insured_database_id: str,
    insured_email: str,
    insured_first_name: str,
    insured_last_name: str,
    insured_commercial_name: str,
    policy_numbers: List[str],
    cost_of_lead: float
) -> Dict:
    """
    Creates a new opportunity in NowCerts via the InsertOpportunity endpoint.
    Automatically handles token generation internally.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = "https://api.nowcerts.com/api/Zapier/InsertOpportunity"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "created_from_renewal": created_from_renewal,
        "line_of_business_name": line_of_business_name,
        "needed_by": needed_by,
        "opportunity_stage_name": opportunity_stage_name,
        "current_stage_due_date": current_stage_due_date,
        "referral_source_name": referral_source_name,
        "referral_source_contact_name": referral_source_contact_name,
        "win_probability": win_probability,
        "agency_commission": agency_commission,
        "assigned_to": assigned_to,
        "description": description,
        "insured_database_id": insured_database_id,
        "insured_email": insured_email,
        "insured_first_name": insured_first_name,
        "insured_last_name": insured_last_name,
        "insured_commercial_name": insured_commercial_name,
        "policy_numbers": policy_numbers,
        "cost_of_lead": cost_of_lead
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "created",
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": "Opportunity creation failed.",
            "details": e.response.json() if e.response else str(e)
        }

def update_opportunity(opportunity_id: str, field: str, value: str) -> Dict:
    return {
        "status": "updated",
        "opportunity_id": opportunity_id,
        "updated_field": field,
        "new_value": value
    }

def add_note_to_opportunity(opportunity_id: str, note: str) -> Dict:
    return {
        "status": "note_added",
        "opportunity_id": opportunity_id,
        "note": note
    }

def add_log_to_opportunity(opportunity_id: str, log: str) -> Dict:
    return {
        "status": "log_added",
        "opportunity_id": opportunity_id,
        "log": log
    }

def add_task_to_opportunity(opportunity_id: str, task_title: str, due_date: str) -> Dict:
    return {
        "status": "task_added",
        "opportunity_id": opportunity_id,
        "task": {
            "title": task_title,
            "due_date": due_date
        }
    }

def get_filtered_opportunities(status: Optional[str] = None, client_name: Optional[str] = None, renewal_before: Optional[str] = None) -> Dict:
    return {
        "status": "fetched",
        "filters": {
            "status": status,
            "client_name": client_name,
            "renewal_before": renewal_before
        },
        "opportunities": []
    }

def get_opportunity_details(opportunity_id: str) -> Dict:
    return {
        "status": "fetched",
        "opportunity_id": opportunity_id,
        "details": {
            "client_name": "John Doe",
            "renewal_date": "2025-06-30",
            "premium": 1200.0
        }
    }

# --- Opportunity Agent Definition ---

opportunity_agent = Agent(
    name="opportunity_agent",
    model="gemini-2.0-flash",
    description="Agent for managing sales and renewal opportunities.",
    instruction="""
You are an Opportunity Management AI Agent.

You can:
- Create renewal opportunities using the NowCerts API.
- Update opportunity fields.
- Add notes, logs, and tasks.
- Fetch filtered opportunities.
- Retrieve specific opportunity details.

Use tools as needed for each user request.
""",
    tools=[
        create_renewal_opportunity,
        update_opportunity,
        add_note_to_opportunity,
        add_log_to_opportunity,
        add_task_to_opportunity,
        get_filtered_opportunities,
        get_opportunity_details,
    ]
)

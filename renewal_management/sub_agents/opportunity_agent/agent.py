from google.adk.agents import Agent
from typing import Optional, Dict, List
import requests
from urllib.parse import quote

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

def update_opportunity(
    database_id: str,
    insured_first_name: Optional[str] = None,
    insured_last_name: Optional[str] = None,
    line_of_business_name: Optional[str] = None,
    needed_by: Optional[str] = None,
    opportunity_stage_name: Optional[str] = None,
    current_stage_due_date: Optional[str] = None,
    referral_source_name: Optional[str] = None,
    referral_source_contact_name: Optional[str] = None,
    win_probability: Optional[str] = None,
    agency_commission: Optional[float] = None,
    assigned_to: Optional[List[str]] = None,
    description: Optional[str] = None,
    insured_database_id: Optional[str] = None,
    insured_email: Optional[str] = None,
    insured_commercial_name: Optional[str] = None,
    policy_numbers: Optional[List[str]] = None,
    cost_of_lead: Optional[float] = None
) -> Dict:
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
        "Content-Type": "application/json"
    }

    body = {
        "database_id": database_id
    }

    optional_fields = {
        "insured_first_name": insured_first_name,
        "insured_last_name": insured_last_name,
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
        "insured_commercial_name": insured_commercial_name,
        "policy_numbers": policy_numbers,
        "cost_of_lead": cost_of_lead
    }

    body.update({k: v for k, v in optional_fields.items() if v is not None})

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return {
            "status": "updated",
            "database_id": database_id,
            "updated_fields": body,
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": "Opportunity update failed.",
            "details": e.response.json() if e.response else str(e)
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

def get_filtered_opportunities(
    opportunity_stage_name: Optional[str] = None,
    insured_first_name: Optional[str] = None,
    insured_last_name: Optional[str] = None,
    needed_by_before: Optional[str] = None,
    skip: int = 0,
    top: int = 10
) -> Dict:
    """
    Fetch opportunities from NowCerts API using supported filter fields.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    base_url = "https://api.nowcerts.com/api/OpportunitiesList"

    # Build $filter string using Insert/Update Opportunity fields
    filters = []
    if opportunity_stage_name:
        filters.append(f"OpportunityStageName eq '{opportunity_stage_name}'")
    if insured_first_name:
        filters.append(f"InsuredFirstName eq '{insured_first_name}'")
    if insured_last_name:
        filters.append(f"InsuredLastName eq '{insured_last_name}'")
    if needed_by_before:
        filters.append(f"NeededBy lt {needed_by_before}")  # Date must be formatted as yyyy-MM-dd

    filter_string = " and ".join(filters)
    encoded_filter = quote(filter_string) if filter_string else ""

    # Final URL with pagination and filtering
    query = f"?$count=true&$orderby=LineOfBusinessName asc&$skip={skip}&$top={top}"
    if encoded_filter:
        query += f"&$filter={encoded_filter}"

    full_url = f"{base_url}(){query}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return {
            "status": "fetched",
            "filters": {
                "opportunity_stage_name": opportunity_stage_name,
                "insured_first_name": insured_first_name,
                "insured_last_name": insured_last_name,
                "needed_by_before": needed_by_before
            },
            "opportunities": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": "Failed to fetch opportunities.",
            "details": e.response.json() if e.response else str(e)
        }

def get_opportunity_details(opportunity_id: str) -> Dict:
    """
    Fetches opportunity details by filtering using the opportunity ID.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = (
        "https://api.nowcerts.com/api/OpportunitiesList"
        f"?$filter=id eq {opportunity_id}"
        "&$count=true&$orderby=id desc&$skip=0&$top=10"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return {
                "status": "fetched",
                "opportunity_id": opportunity_id,
                "details": data[0]  # return the first matching result
            }
        else:
            return {
                "status": "not_found",
                "opportunity_id": opportunity_id,
                "message": "No opportunity found with the given ID."
            }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": "Failed to fetch opportunity details.",
            "details": e.response.json() if e.response else str(e)
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

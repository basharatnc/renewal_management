import os
from google.adk.agents import Agent
from typing import Optional, Dict, List
import requests
from urllib.parse import quote
import json
from datetime import datetime
from utils import get_access_token
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NC_API_BASE_URL = os.getenv("NC_API_BASE_URL")

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

    url = f"{NC_API_BASE_URL}/Zapier/InsertOpportunity"
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
    Updates an existing opportunity in NowCerts via the InsertOpportunity endpoint.
    Requires a valid database_id to update the specified opportunity fields.
    All fields are required to match the create function's behavior and ensure compatibility.
    """
    try:
        access_token = get_access_token()
        print(f"Access Token (partial): {access_token[:10]}...")  # Log partial token for debugging
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = f"{NC_API_BASE_URL}/Zapier/InsertOpportunity"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Ensure proper type handling
    if isinstance(needed_by, datetime):
        needed_by = needed_by.strftime("%m/%d/%Y")
    if isinstance(current_stage_due_date, datetime):
        current_stage_due_date = current_stage_due_date.strftime("%m/%d/%Y")
    if agency_commission is not None:
        agency_commission = float(agency_commission)
    if cost_of_lead is not None:
        cost_of_lead = float(cost_of_lead)

    payload = {
        "database_id": database_id,
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
            "status": "updated",
            "database_id": database_id,
            "updated_fields": payload,
            "response": response.json()
        }
    except requests.RequestException as e:
        error_details = e.response.json() if e.response else str(e)
        print(f"API Error: Status Code: {e.response.status_code if e.response else 'No response'}, Details: {json.dumps(error_details, indent=2)}")
        return {
            "status": "error",
            "message": "Opportunity update failed.",
            "details": error_details
        }
    
def add_log_to_opportunity(opportunity_id: str, log: str) -> Dict:
    return {
        "status": "log_added",
        "opportunity_id": opportunity_id,
        "log": log
    }

def add_task_to_opportunity(
    opportunity_database_id: str,
    title: str,
    due_date: str,
    description: Optional[str] = None,
    status: Optional[str] = "Not Started",
    completion: Optional[int] = 0,
    priority: Optional[str] = "medium",
    assigned_to: Optional[List[str]] = None,
    insured_database_id: Optional[str] = None,
    creator_name: Optional[str] = "Opportunity Agent"
) -> Dict:
    """
    Adds a detailed task to a specified opportunity in NowCerts using the InsertTask endpoint.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = f"{NC_API_BASE_URL}/Zapier/InsertTask"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "CreatorName": creator_name,
        "title": title,
        "description": description or "",
        "status": status,
        "completion": completion,
        "priority": priority,
        "due_date": due_date,
        "assigned_to": assigned_to or [],
        "opportunity_database_id": opportunity_database_id,
        "insured_database_id": insured_database_id
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return {
            "status": "task_added",
            "opportunity_database_id": opportunity_database_id,
            "task": body,
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": "Failed to add task to opportunity.",
            "details": e.response.json() if e.response else str(e)
        }

def get_filtered_opportunities(
    id: Optional[str] = None,
    line_of_business_name: Optional[str] = None,
    opportunity_stage_name: Optional[str] = None,
    needed_by: Optional[str] = None,
    current_stage_due_date: Optional[str] = None,
    referral_source_name: Optional[str] = None,
    referral_source_contact_name: Optional[str] = None,
    win_probability: Optional[str] = None,
    agency_commission: Optional[float] = None,
    assigned_to: Optional[List[str]] = None,
    description: Optional[str] = None,
    insured_commercial_name: Optional[str] = None,
    insured_email: Optional[str] = None,
    policy_numbers: Optional[List[str]] = None,
    created_from_renewal: Optional[bool] = None,
    create_date: Optional[str] = None,
    change_date: Optional[str] = None,
    last_change_user_name: Optional[str] = None
) -> Dict:
    """
    Fetches opportunity details by filtering using the provided criteria.
    Returns both raw details and a bullet-style formatted string.
    All parameters are optional to allow flexible filtering.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = f"{NC_API_BASE_URL}/Zapier/OpportunitiesList"
    filter_criteria = {
        "id": id,
        "lineOfBusinessName": line_of_business_name,
        "opportunityStageName": opportunity_stage_name,
        "neededBy": needed_by,
        "currentStageDueDate": current_stage_due_date,
        "referralSourceName": referral_source_name,
        "referralSourceContactName": referral_source_contact_name,
        "winProbability": win_probability,
        "agencyCommission": agency_commission,
        "assignedTo": assigned_to,
        "description": description,
        "insuredCommercialName": insured_commercial_name,
        "insuredEmail": insured_email,
        "policyNumbers": policy_numbers,
        "createdFromRenewal": created_from_renewal,
        "createDate": create_date,
        "changeDate": change_date,
        "lastChangeUserName": last_change_user_name
    }

    # Construct OData $filter query from non-None criteria
    filter_parts = []
    for field, value in filter_criteria.items():
        if value is not None:
            if isinstance(value, str):
                filter_parts.append(f"{field} eq '{value}'")
            elif isinstance(value, bool):
                filter_parts.append(f"{field} eq {str(value).lower()}")
            elif isinstance(value, (int, float)):
                filter_parts.append(f"{field} eq {value}")
            elif isinstance(value, list):
                value_str = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in value])
                filter_parts.append(f"{field}/any(x: x in ({value_str}))")
    filter_query = " and ".join(filter_parts) if filter_parts else ""

    params = {
        "$filter": filter_query,
        "$count": "true",
        "$orderby": "id desc",
        "$skip": "0",
        "$top": "3"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "value" in data and data["value"]:
            opportunity = data["value"][0]

            formatted_output = "\n".join([
                f"• Line of Business: {opportunity.get('lineOfBusinessName')}",
                f"• Opportunity Stage: {opportunity.get('opportunityStageName')}",
                f"• Needed By: {opportunity.get('neededBy')}",
                f"• Current Stage Due Date: {opportunity.get('currentStageDueDate')}",
                f"• Referral Source: {opportunity.get('referralSourceName')}",
                f"• Referral Contact: {opportunity.get('referralSourceContactName')}",
                f"• Win Probability: {opportunity.get('winProbability')}",
                f"• Agency Commission: {opportunity.get('agencyCommission')}%",
                f"• Assigned To: {', '.join(opportunity.get('assignedTo', []))}",
                f"• Description: {opportunity.get('description')}",
                f"• Insured Commercial Name: {opportunity.get('insuredCommercialName')}",
                f"• Insured Email: {opportunity.get('insuredEmail')}",
                f"• Policy Numbers: {', '.join(opportunity.get('policyNumbers', []))}",
                f"• Created From Renewal: {opportunity.get('createdFromRenewal')}",
                f"• Created On: {opportunity.get('createDate')}",
                f"• Last Changed On: {opportunity.get('changeDate')}",
                f"• Last Changed By: {opportunity.get('lastChangeUserName')}"
            ])

            return {
                "status": "fetched",
                "filter_criteria": filter_criteria,
                "details": opportunity,
                "formatted": formatted_output
            }
        else:
            return {
                "status": "not_found",
                "filter_criteria": filter_criteria,
                "message": "No opportunity found with the given filter criteria."
            }

    except requests.RequestException as e:
        error_details = e.response.json() if e.response else str(e)
        print(f"API Error: Status Code: {e.response.status_code if e.response else 'No response'}, Details: {json.dumps(error_details, indent=2)}")
        return {
            "status": "error",
            "message": "Failed to fetch opportunity details.",
            "details": error_details
        }
        
def get_opportunity_details(opportunity_id: str) -> Dict:
    """
    Fetches opportunity details by filtering using the opportunity ID.
    Returns both raw details and a bullet-style formatted string.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = f"{NC_API_BASE_URL}/Zapier/OpportunitiesList"
    params = {
        "$filter": f"id eq {opportunity_id}",
        "$count": "true",
        "$orderby": "id desc",
        "$skip": "0",
        "$top": "1"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "value" in data and data["value"]:
            opportunity = data["value"][0]

            formatted_output = "\n".join([
                f"• Line of Business: {opportunity.get('lineOfBusinessName')}",
                f"• Opportunity Stage: {opportunity.get('opportunityStageName')}",
                f"• Needed By: {opportunity.get('neededBy')}",
                f"• Current Stage Due Date: {opportunity.get('currentStageDueDate')}",
                f"• Referral Source: {opportunity.get('referralSourceName')}",
                f"• Referral Contact: {opportunity.get('referralSourceContactName')}",
                f"• Win Probability: {opportunity.get('winProbability')}",
                f"• Agency Commission: {opportunity.get('agencyCommission')}%",
                f"• Assigned To: {', '.join(opportunity.get('assignedTo', []))}",
                f"• Description: {opportunity.get('description')}",
                f"• Insured Commercial Name: {opportunity.get('insuredCommercialName')}",
                f"• Insured Email: {opportunity.get('insuredEmail')}",
                f"• Policy Numbers: {', '.join(opportunity.get('policyNumbers', []))}",
                f"• Created From Renewal: {opportunity.get('createdFromRenewal')}",
                f"• Created On: {opportunity.get('createDate')}",
                f"• Last Changed On: {opportunity.get('changeDate')}",
                f"• Last Changed By: {opportunity.get('lastChangeUserName')}"
            ])

            return {
                "status": "fetched",
                "opportunity_id": opportunity_id,
                "details": opportunity,
                "formatted": formatted_output
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
    description="Agent for managing opportunities.",
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
        add_log_to_opportunity,
        add_task_to_opportunity,
        get_filtered_opportunities,
        get_opportunity_details,
    ]
)

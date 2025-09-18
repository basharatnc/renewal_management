import os
from google.adk.agents import Agent
from typing import Optional, Dict, List
import requests
from urllib.parse import quote
import json
from datetime import datetime
from utils import get_access_token
from dotenv import load_dotenv
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

NC_API_BASE_URL = os.getenv("NC_API_BASE_URL")

# --- Tool Functions ---

def create_service_request_policy_change(
    subject: str,
    status: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    service_request_id: Optional[str] = None,
    insured_id: Optional[str] = None,
    insured_name: Optional[str] = None,
    insured_email: Optional[str] = None,
    insured_phone: Optional[str] = None,
    policy_database_id: Optional[List[str]] = None,
    request_database_id: Optional[str] = None
) -> Dict:
    """
    Creates or updates a service request for a policy change in NowCerts.

    Parameters:
        subject (str): The subject of the service request.
        status (str): The status of the service request (e.g., 'New', 'In Progress', 'Completed').
        description (Optional[str]): A detailed description of the service request.
        due_date (Optional[str]): The due date for the request (e.g., 'MM/DD/YYYY').
        service_request_id (Optional[str]): A unique ID for the service request.
        insured_id (Optional[str]): The primary key of the insured in the NowCerts system.
        insured_name (Optional[str]): The name of the insured.
        insured_email (Optional[str]): The email address of the insured.
        insured_phone (Optional[str]): The phone number of the insured.
        policy_database_id (Optional[List[str]]): A list of primary keys for policies related to the request.
        request_database_id (Optional[str]): The primary key of the service request to be updated.

    Returns:
        dict: A dictionary containing the status of the request and the response from the API.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = f"{NC_API_BASE_URL}/Zapier/InsertServiceRequestsPolicyChange"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Prepare payload with all provided parameters
    payload = {
        "subject": subject,
        "status": status,
    }
    
    if description:
        payload["description"] = description
    if due_date:
        # Convert datetime object to string if necessary
        if isinstance(due_date, datetime):
            due_date = due_date.strftime("%m/%d/%Y")
        payload["due_date"] = due_date
    if service_request_id:
        payload["service_request_id"] = service_request_id
    if insured_id:
        payload["insured_id"] = insured_id
    if insured_name:
        payload["insured_name"] = insured_name
    if insured_email:
        payload["insured_email"] = insured_email
    if insured_phone:
        payload["insured_phone"] = insured_phone
    if policy_database_id:
        payload["policy_database_id"] = policy_database_id
    if request_database_id:
        payload["request_database_id"] = request_database_id

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "response": response.json()
        }
    except requests.RequestException as e:
        error_details = e.response.json() if e.response and hasattr(e.response, 'json') else str(e)
        return {
            "status": "error",
            "message": "Service request creation/update failed.",
            "details": error_details
        }
 
def list_service_requests_policy_change(
    count: bool,
    orderby: str,
    skip: int,
    top: int,
    filter_by: Optional[str] = None
) -> Dict:
    """
    Retrieves a list of policy change service requests from NowCerts.

    Parameters:
        count (bool): Whether to return the total number of records.
        orderby (str): The parameter to order the results by (e.g., 'changeDate').
        skip (int): The number of records to skip for pagination.
        top (int): The number of records to retrieve.
        filter_by (Optional[str]): An OData filter string to narrow down the results (e.g., "subject eq 'subject'").

    Returns:
        Dict: A dictionary containing the status and the response from the API.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = f"{NC_API_BASE_URL}/ServiceRequestsPolicyChangeList"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    params = {
        "$count": "true" if count else "false",
        "$orderby": orderby,
        "$skip": skip,
        "$top": top
    }
    
    if filter_by:
        params["$filter"] = filter_by

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return {
            "status": "success",
            "response": response.json()
        }
    except requests.RequestException as e:
        error_details = e.response.json() if e.response else str(e)
        return {
            "status": "error",
            "message": "Failed to retrieve policy change service requests.",
            "details": error_details
        }


def update_service_request_policy_change(
    request_database_id: str,
    subject: Optional[str] = None,
    status: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    service_request_id: Optional[str] = None,
    insured_id: Optional[str] = None,
    insured_name: Optional[str] = None,
    insured_email: Optional[str] = None,
    insured_phone: Optional[str] = None,
    policy_database_id: Optional[List[str]] = None
) -> Dict:
    """
    Updates an existing service request for a policy change in NowCerts.

    Parameters:
        request_database_id (str): The primary key of the service request to be updated. This is a required field.
        subject (Optional[str]): The subject of the service request.
        status (Optional[str]): The status of the service request (e.g., 'New', 'In Progress', 'Completed').
        description (Optional[str]): A detailed description of the service request.
        due_date (Optional[str]): The due date for the request (e.g., 'MM/DD/YYYY').
        service_request_id (Optional[str]): A unique ID for the service request.
        insured_id (Optional[str]): The primary key of the insured in the NowCerts system.
        insured_name (Optional[str]): The name of the insured.
        insured_email (Optional[str]): The email address of the insured.
        insured_phone (Optional[str]): The phone number of the insured.
        policy_database_id (Optional[List[str]]): A list of primary keys for policies related to the request.

    Returns:
        Dict: A dictionary containing the status of the request and the response from the API.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    url = f"{NC_API_BASE_URL}/Zapier/InsertServiceRequestsPolicyChange"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


    payload = {
        "request_database_id": request_database_id
    }
    
    if subject:
        payload["subject"] = subject
    if status:
        payload["status"] = status
    if description:
        payload["description"] = description
    if due_date:
        if isinstance(due_date, datetime):
            due_date = due_date.strftime("%m/%d/%Y")
        payload["due_date"] = due_date
    if service_request_id:
        payload["service_request_id"] = service_request_id
    if insured_id:
        payload["insured_id"] = insured_id
    if insured_name:
        payload["insured_name"] = insured_name
    if insured_email:
        payload["insured_email"] = insured_email
    if insured_phone:
        payload["insured_phone"] = insured_phone
    if policy_database_id:
        payload["policy_database_id"] = policy_database_id

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "response": response.json()
        }
    except requests.RequestException as e:
        error_details = e.response.json() if e.response else str(e)
        return {
            "status": "error",
            "message": "Service request update failed.",
            "details": error_details
        }   
        
        
def get_service_request_details(service_request_id: str) -> Dict:
    """
    Fetches the details of a specific policy change service request by filtering using its ID.

    Parameters:
        service_request_id (str): The unique ID of the service request.

    Returns:
        Dict: A dictionary containing the status and the details of the service request.
    """
    try:
        access_token = get_access_token()
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve access token.",
            "details": str(e)
        }

    base_url = f"{NC_API_BASE_URL}/ServiceRequestsPolicyChangeList"
    query_params = {
        "$filter": f"id eq {service_request_id}",
        "$count": "true",
        "$orderby": "createDate desc",
        "$skip": "0",
        "$top": "1"
    }

    # Manually encode, preserving $ symbols
    query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
    url = f"{base_url}?{query_string}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "value" in data and data["value"]:
            service_request = data["value"][0]

            formatted_output = "\n".join([
                f"• Subject: {service_request.get('subject')}",
                f"• Description: {service_request.get('description')}",
                f"• Status: {service_request.get('status')}",
                f"• Created On: {service_request.get('createDate')}",
                f"• Last Changed On: {service_request.get('changeDate')}",
                f"• Due By: {service_request.get('dueDate')}",
                f"• Service Request ID: {service_request.get('serviceRequestId')}",
                f"• Insured Name: {service_request.get('insuredName')}",
                f"• Insured Email: {service_request.get('insuredEmail')}"
            ])
            
            # Handling policies list
            policies = service_request.get('policies')
            if policies:
                policy_details = []
                for policy in policies:
                    lob = ", ".join(policy.get('linesOfBusiness', []))
                    policy_details.append(
                        f"  - Policy Number: {policy.get('number', 'N/A')}\n"
                        f"  - Line of Business: {lob}\n"
                        f"  - Carrier: {policy.get('carrierName', 'N/A')}"
                    )
                formatted_output += "\n• Associated Policies:\n" + "\n".join(policy_details)
                
            return {
                "status": "fetched",
                "service_request_id": service_request_id,
                "details": service_request,
                "formatted": formatted_output
            }
        else:
            return {
                "status": "not_found",
                "service_request_id": service_request_id,
                "message": "No service request found with the given ID."
            }

    except requests.RequestException as e:
        return {
            "status": "error",
            "message": "Failed to fetch service request details.",
            "details": e.response.json() if e.response else str(e)
        }
    
# --- Endorsement Agent Definition ---

endorsement_agent = Agent(
    name="endorsement_agent",
    model="gemini-2.0-flash",
    description="Agent for managing endorsements via service requests (policy changes).",
    instruction="""
You are an Endorsement Management AI Agent.

You can:
- Create or update service requests for policy changes using the NowCerts API.
- List service requests with optional filtering.
- Fetch details of a specific service request.
- Update existing service requests.

Use tools as needed for each user request.
""",
    tools=[
        create_service_request_policy_change,
        list_service_requests_policy_change,
        get_service_request_details,
        update_service_request_policy_change,
    ]
)
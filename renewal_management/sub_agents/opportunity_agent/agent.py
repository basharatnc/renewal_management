from google.adk.agents import Agent
from typing import Optional, Dict

# --- Tool Functions ---

def create_renewal_opportunity(opportunity_id: str, client_name: str, renewal_date: str, premium: float) -> Dict:
    return {
        "status": "created",
        "opportunity_id": opportunity_id,
        "details": {
            "client_name": client_name,
            "renewal_date": renewal_date,
            "premium": premium
        }
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
- Create renewal opportunities.
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

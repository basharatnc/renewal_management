from google.adk.agents import Agent
from typing import Dict
import re
import requests

# --- Tool 1: Identify Policy Issuance Intent ---
def identify_policy_issuance_intent(email_text: str) -> dict:
    """
    Detect if the incoming email expresses an intent to issue a new policy.
    """
    keywords = ["issue policy", "new policy", "need policy", "please issue", "policy request"]
    detected = any(kw in email_text.lower() for kw in keywords)
    return {
        "intent_detected": detected,
        "intent_type": "PolicyIssuance" if detected else "Unknown",
        "confidence": 0.95 if detected else 0.1
    }

# --- Tool 2: Generate Mail Body using LLM ---
def generate_mail_body(policy_info: dict) -> dict:
    """
    Generate a formal email body based on provided policy information.
    """
    insured_name = policy_info.get("insured_name", "Client")
    policy_type = policy_info.get("policy_type", "General Insurance")
    policy_number = policy_info.get("policy_number", "N/A")
    effective_date = policy_info.get("effective_date", "N/A")
    expiration_date = policy_info.get("expiration_date", "N/A")
    premium_amount = policy_info.get("premium_amount", "N/A")
    carrier_name = policy_info.get("carrier_name", "N/A")

    body = f"""Dear {insured_name},

    We are pleased to inform you that your {policy_type} policy has been successfully issued.

    Here are the details of your policy:

    • Policy Number   : {policy_number}  
    • Effective Date  : {effective_date}  
    • Expiration Date : {expiration_date}  
    • Premium Amount  : ${premium_amount}  
    • Carrier         : {carrier_name}

    If you have any questions or need further assistance, please feel free to contact us.

    Best regards,  
    Momentum AMP"""

    return {"mail_body": body}

# --- Tool 3: Send Mail using MAC (Mock version) ---
def send_mail(recipient: str, subject: str, body: str) -> dict:
    """
    Sends an email using the FusionNow CRM email API.
    """
    url = "https://staging.api.fusionnowcrm.com/api/open_api/v1/fusion_actions/send_email.json"
    headers = {
        "Content-Type": "application/json",
        "api-secret": "4eb46e76f89c1cdc6085e3a39794f5ed4374dee0157e393d9c7a2a7fc74f"
    }
    payload = {
        "email": recipient,
        "subject": subject,
        "body": body
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "recipient": recipient,
            "subject": subject,
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": "Failed to send email.",
            "details": str(e),
            "response": e.response.json() if e.response else None
        }

# Communication Agent Definition
communication_agent = Agent(
    name="communication_agent",
    model="gemini-2.0-flash",
    description="Handles detection and responses for policy issuance requests.",
    instruction="""
You are a Communication Management AI Agent.

Your responsibilities:
1. Detect if an incoming email contains a 'Policy Issuance' intent.
2. If detected, use the policy information to generate a formal response.
3. Send the response email using the send_mail tool.

Use tools in this order:
1. identify_policy_issuance_intent
2. generate_mail_body
3. send_mail
""",
    tools=[
        identify_policy_issuance_intent,
        generate_mail_body,
        send_mail
    ]
)

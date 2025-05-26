from google.adk.agents import Agent
from typing import Dict
import re

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

    body = f"""Dear {insured_name},

We are pleased to inform you that your {policy_type} policy has been successfully issued.

Please find the policy document attached. Let us know if you have any questions.

Best regards,  
Momentum AMP"""
    
    return {"mail_body": body}

# --- Tool 3: Send Mail using MAC (Mock version) ---
def send_mail(recipient: str, subject: str, body: str) -> dict:
    """
    Simulates sending an email. Replace with real mail service integration in production.
    """
    print(f"\n--- SENDING EMAIL ---")
    print(f"To      : {recipient}")
    print(f"Subject : {subject}")
    print(f"Body    :\n{body}")
    print(f"--- EMAIL SENT ---\n")
    return {"status": "sent", "recipient": recipient, "subject": subject}

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

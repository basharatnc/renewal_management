import uuid
import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uvicorn
from renewal_management.agent import root_agent

# Load environment variables
load_dotenv()

app = FastAPI()

# Persistent session state
session_service = InMemorySessionService()

# Constants
APP_NAME = "Manager Agent"
USER_ID = "basharat_hussain"
SESSION_ID = str(uuid.uuid4())

# Initialize the session when app starts

# Input model
class Question(BaseModel):
    message: str

# Ask endpoint
@app.post("/ask")
async def ask_question(q: Question):   
    # Check if session exists
    existing_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    
    if not existing_session:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )
        print(f"✅ Session created: {SESSION_ID}")
    else:
        print(f"ℹ️ Reusing session: {SESSION_ID}")

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part(text=q.message)]
    )

    full_response = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            full_response = event.content.parts[0].text

    return {"response": full_response}

if __name__ == "__main__":
    uvicorn.run(
        "fastapi_app:app", 
        host="localhost", 
        port=8000,
        reload=True
    )

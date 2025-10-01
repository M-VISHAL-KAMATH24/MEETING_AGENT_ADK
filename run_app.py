import asyncio
import sys
import os
from dotenv import load_dotenv

# --- Step 1: Load Environment Variables & Import ADK ---
dotenv_path = os.path.join(os.path.dirname(__file__), 'coordinator_agent', '.env')
load_dotenv(dotenv_path=dotenv_path)

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types
from google.adk.memory import InMemoryMemoryService

# --- Step 2: Import Your Agents and the New Whisper Transcriber ---
sys.path.append('..')
from coordinator_agent.agent import root_agent as coordinator_agent
from transcriber_whisper import run_transcription  # Import our new function

# --- Step 3: Initialize Services & Runner (No Changes) ---
memory_service = InMemoryMemoryService()
session_service = InMemorySessionService()

runner = Runner(
    agent=coordinator_agent,
    session_service=session_service,
    memory_service=memory_service,
    app_name="AI_Meeting_Assistant"
)

# --- Step 4: Define the Main Application Logic (No Changes) ---
async def process_user_command(user_input, user_id, session_id):
    """Takes transcribed text and sends it to the ADK runner."""
    print(f"PROCESSING: '{user_input}'")
    message = genai_types.Content(
        role='user',
        parts=[genai_types.Part(text=user_input)]
    )
    final_response_text = ""
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=message):
        if event.is_final_response():
            final_response_text = event.content.parts[0].text
    
    if final_response_text:
        print(f"[ASSISTANT]: {final_response_text}\n")

# --- Step 5: The New Main Entry Point ---
async def main():
    print("AI Meeting Assistant with LOCAL Whisper Transcription is running...")
    
    user_id = "live_user"
    session = await session_service.create_session(app_name=runner.app_name, user_id=user_id)

    callback = lambda transcript: asyncio.run(
        process_user_command(transcript, user_id, session.id)
    )

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, run_transcription, callback)

# --- Step 6: Run the Application (No Changes) ---
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")

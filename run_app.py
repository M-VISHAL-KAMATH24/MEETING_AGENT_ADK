import asyncio
import sys
import os
from dotenv import load_dotenv

# --- Step 1: Load Environment Variables ---
# We load the .env file from the coordinator_agent directory.
# This makes the GOOGLE_API_KEY available to the entire application.
dotenv_path = os.path.join(os.path.dirname(__file__), 'coordinator_agent', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Now that the environment is set, we can import the ADK modules.
from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types

# --- Step 2: Import Your Coordinator Agent ---
# This remains the same.
sys.path.append('..')
from coordinator_agent.agent import root_agent as coordinator_agent

# --- Step 3: Initialize Services ---
# This also remains the same.
memory_service = InMemoryMemoryService()
session_service = InMemorySessionService()

# --- Step 4: Create a Runner ---
# This also remains the same.
runner = Runner(
    agent=coordinator_agent,
    session_service=session_service,
    memory_service=memory_service,
    app_name="AI_Meeting_Assistant"
)

# --- Step 5: The Main ASYNC Chat Loop ---
async def main():
    print("AI Meeting Assistant with Shared Memory is running...")
    print("Type 'exit' to quit.")

    user_id = "local_user"
    session = await session_service.create_session(app_name=runner.app_name, user_id=user_id)

    while True:
        loop = asyncio.get_running_loop()
        user_input = await loop.run_in_executor(None, input, "[user]: ")

        if user_input.lower() == "exit":
            break

        message = genai_types.Content(
            role='user',
            parts=[genai_types.Part(text=user_input)]
        )

        final_response_text = ""
        # The runner.run() method returns a generator, so we loop over it.
        for event in runner.run(user_id=user_id, session_id=session.id, new_message=message):
            if event.is_final_response():
                final_response_text = event.content.parts[0].text
        
        if final_response_text:
            print(f"[assistant]: {final_response_text}")

# --- Step 6: Run the Application ---
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")


import sys
from google.adk.agents import Agent
from google.adk.tools import agent_tool

# --- Step 1: Import Your Specialist Agents (No Changes) ---
sys.path.append('..')
from note_taker_agent.agent import root_agent as note_taker_agent
from agenda_tracker_agent.agent import root_agent as agenda_tracker_agent


# --- Step 2: Wrap the Agents as Tools (Corrected) ---
# We do NOT pass a 'name' argument. The tool's name will be derived
# from the 'name' attribute inside the specialist agent's definition.
note_taker_as_tool = agent_tool.AgentTool(agent=note_taker_agent)
agenda_tracker_as_tool = agent_tool.AgentTool(agent=agenda_tracker_agent)


# --- Step 3: Define the Coordinator Agent ---
# The instructions here will now perfectly match the names of the tools
# because we simplified the names in the specialist agents' files.
root_agent = Agent(
    name="meeting_coordinator",
    model="gemini-2.0-flash",
    description="The main coordinator for the AI Meeting Assistant.",
    instruction="""
    You are the lead coordinator for a meeting. Your job is to understand the user's request and delegate it to the correct specialist agent.

    - If the user's request is about taking a note or remembering an action item,
      you MUST use the `note_taker_agent` tool.

    - If the user's request is about the meeting agenda,
      you MUST use the `agenda_tracker_agent` tool.

    Do not try to answer the questions yourself. Your only job is to route the request.
    """,
    tools=[
        note_taker_as_tool,
        agenda_tracker_as_tool
    ]
)

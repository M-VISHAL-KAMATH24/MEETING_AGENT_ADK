import sys
from google.adk.agents import Agent
from google.adk.tools import agent_tool


# --- Step 1: Import All Your Specialist Agents ---
sys.path.append('..')
from note_taker_agent.agent import root_agent as note_taker_agent
from agenda_tracker_agent.agent import root_agent as agenda_tracker_agent
# Import the new Calendar Agent
from calendar_agent.agent import root_agent as calendar_agent


# --- Step 2: Wrap All Agents as Tools ---
# The tool's name will be derived from the 'name' attribute
# inside each specialist agent's definition.
note_taker_as_tool = agent_tool.AgentTool(agent=note_taker_agent)
agenda_tracker_as_tool = agent_tool.AgentTool(agent=agenda_tracker_agent)
# Wrap the new Calendar Agent
calendar_as_tool = agent_tool.AgentTool(agent=calendar_agent)


# --- Step 3: Define the Updated Coordinator Agent ---
# The instructions and tools list are updated to include the new calendar capability.
root_agent = Agent(
    name="meeting_coordinator",
    model="gemini-2.0-flash",
    description="The main coordinator for the AI Meeting Assistant.",
    instruction="""
    You are the lead coordinator for a meeting. Your job is to understand the user's request and delegate it to the correct specialist agent.

    - If the user's request is about taking a note or remembering an action item,
      you MUST use the `note_taker_agent` tool.

    - If the user's request is about the meeting agenda (reading it, asking what's next, etc.),
      you MUST use the `agenda_tracker_agent` tool.

    - If the user's request is about their schedule, upcoming events, or what is on their calendar,
      you MUST use the `calendar_agent` tool.

    Do not try to answer the questions yourself. Your only job is to route the request to the correct tool.
    """,
    tools=[
        note_taker_as_tool,
        agenda_tracker_as_tool,
        calendar_as_tool  # Add the new tool to the list
    ]
)

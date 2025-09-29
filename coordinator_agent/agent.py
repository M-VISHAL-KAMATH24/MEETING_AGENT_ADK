import sys
from google.adk.agents import Agent
from google.adk.tools import agent_tool


# --- Step 1: Import All Your Specialist Agents ---
sys.path.append('..')
from note_taker_agent.agent import root_agent as note_taker_agent
from agenda_tracker_agent.agent import root_agent as agenda_tracker_agent
from calendar_agent.agent import root_agent as calendar_agent
# Import the new Email Agent
from email_agent.agent import root_agent as email_agent


# --- Step 2: Wrap All Agents as Tools ---
# The tool's name is derived from the 'name' attribute inside each agent's definition.
note_taker_as_tool = agent_tool.AgentTool(agent=note_taker_agent)
agenda_tracker_as_tool = agent_tool.AgentTool(agent=agenda_tracker_agent)
calendar_as_tool = agent_tool.AgentTool(agent=calendar_agent)
# Wrap the new Email Agent
email_as_tool = agent_tool.AgentTool(agent=email_agent)


# --- Step 3: Define the Final Coordinator Agent ---
# The instructions and tools list are updated to include all four agents.
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
      
    - If the user asks to send a follow-up email or the meeting summary,
      you MUST use the `email_agent` tool.

    Do not try to answer the questions yourself. Your only job is to route the request to the correct tool.
    """,
    tools=[
        note_taker_as_tool,
        agenda_tracker_as_tool,
        calendar_as_tool,
        email_as_tool  # Add the final tool to the list
    ]
)

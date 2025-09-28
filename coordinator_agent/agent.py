from google.adk.agents import Agent
from google.adk.tools import agent_tool

# --- Step 1: Import Your Specialist Agents ---
# The ADK needs to know where to find your other agents.
# We add their parent directories to the Python path.
import sys
sys.path.append('..')

# Now, we can import the `root_agent` variable from each agent's script.
from note_taker_agent.agent import root_agent as note_taker_agent
from agenda_tracker_agent.agent import root_agent as agenda_tracker_agent


# --- Step 2: Wrap the Agents as Tools ---
# The `agent_tool.AgentTool` class makes an entire agent look like
# a single tool that the Coordinator can call.
note_taker_as_tool = agent_tool.AgentTool(agent=note_taker_agent)
agenda_tracker_as_tool = agent_tool.AgentTool(agent=agenda_tracker_agent)


# --- Step 3: Define the Coordinator Agent ---
# This agent's only job is to delegate tasks.

root_agent = Agent(
    name="meeting_coordinator",
    model="gemini-2.0-flash",
    description="The main coordinator for the AI Meeting Assistant. It delegates tasks to specialist agents.",
    instruction="""
    You are the lead coordinator for a meeting. Your job is to understand the user's request and delegate it to the correct specialist agent.

    - If the user's request is about taking a note or remembering an action item,
      you MUST use the `note_taker_agent` tool.

    - If the user's request is about the meeting agenda (reading it, asking what's next, etc.),
      you MUST use the `agenda_tracker_agent` tool.

    Do not try to answer the questions yourself. Your only job is to route the request to the correct tool.
    """,
    # The Coordinator's toolbox contains other agents!
    tools=[
        note_taker_as_tool,
        agenda_tracker_as_tool
    ]
)

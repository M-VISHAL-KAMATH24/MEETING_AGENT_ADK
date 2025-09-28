import os
from google.adk.agents import Agent

# --- The rest of your code remains the same ---

meeting_state = {
    "agenda": [],
    "current_item_index": -1
}

# --- Tool 1: Read the agenda (Corrected Version) ---

def read_the_full_agenda() -> dict:
    """
    Reads the meeting agenda from the 'agenda.txt' file,
    stores it in memory, and returns the full agenda.
    This should be the first tool called in any meeting.
    """
    try:
        # Get the directory where this python script is located
        script_dir = os.path.dirname(__file__)
        
        # Create the full path to the agenda.txt file
        file_path = os.path.join(script_dir, 'agenda.txt')
        
        print(f"DEBUG: Attempting to read agenda from: {file_path}")

        with open(file_path, 'r') as f:
            agenda_items = [line.strip() for line in f.readlines()]
        
        meeting_state["agenda"] = agenda_items
        meeting_state["current_item_index"] = -1
        
        return {"status": "success", "agenda": agenda_items}
    except FileNotFoundError:
        # Return a more specific error message
        return {"status": "error", "message": "The 'agenda.txt' file was not found. Please ensure it is in the same folder as the agent.py script."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- The rest of your code (Tool 2 and Agent Definition) remains the same ---
def get_next_agenda_item() -> dict:
    """
    Gets the next item from the agenda that is stored in memory.
    Call this when the user asks 'what's next?' or to move on.
    """
    if not meeting_state["agenda"]:
        return {"status": "error", "message": "The agenda has not been read yet. Please call 'read_the_full_agenda' first."}
        
    meeting_state["current_item_index"] += 1
    
    index = meeting_state["current_item_index"]
    
    if index < len(meeting_state["agenda"]):
        next_item = meeting_state["agenda"][index]
        return {"status": "success", "next_item": next_item}
    else:
        return {"status": "finished", "message": "We have reached the end of the agenda."}

root_agent = Agent(
    name="agenda_tracker_agent",
    model="gemini-2.0-flash",
    description="An agent that can read an agenda and track progress item by item.",
    instruction="""
    You are an expert meeting facilitator. Your job is to manage the agenda.
    
    1.  If the user asks to see or start the agenda, you MUST call the `read_the_full_agenda` tool first.
    2.  When the user asks "what's next?" or to move on, you MUST call the `get_next_agenda_item` tool.
    3.  Politely inform the user if they try to get the next item before reading the agenda first.
    """,
    tools=[read_the_full_agenda, get_next_agenda_item]
)


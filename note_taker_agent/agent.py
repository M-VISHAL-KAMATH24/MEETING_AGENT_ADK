import datetime
from google.adk.agents import Agent
# --- Tool 1: For saving general notes ---

def save_note(note: str) -> dict:
    """
    Saves a given text note to a file named 'meeting_notes.txt'.

    Args:
        note (str): The text content to be saved as a note.

    Returns:
        A dictionary confirming the status of the operation.
    """
    try:
        filename = f"meeting_notes_{datetime.date.today()}.txt"
        with open(filename, 'a') as f:
            f.write(f"- {note}\\n")
        
        print(f"DEBUG: Note '{note}' saved to {filename}")
        return {"status": "success", "message": f"Note saved to {filename}."}
        
    except Exception as e:
        print(f"ERROR: Failed to save note. {e}")
        return {"status": "error", "message": str(e)}

# --- Tool 2: For saving specific action items ---

def save_action_item(action_item: str) -> dict:
    """
    Saves a specific action item to a file named 'action_items.txt'.

    Args:
        action_item (str): The text of the action item to be saved.
    
    Returns:
        A dictionary confirming the status of the operation.
    """
    try:
        filename = f"action_items_{datetime.date.today()}.txt"
        with open(filename, 'a') as f:
            f.write(f"- {action_item}\\n")
        
        print(f"DEBUG: Action Item '{action_item}' saved to {filename}")
        return {"status": "success", "message": f"Action item saved to {filename}."}
        
    except Exception as e:
        print(f"ERROR: Failed to save action item. {e}")
        return {"status": "error", "message": str(e)}


# --- The Enhanced Agent Definition ---

root_agent = Agent(
    name="note_taker_agent",
    model="gemini-2.0-flash",
    description="An agent that saves notes and also identifies and saves action items.",
    instruction="""
    You are an intelligent meeting assistant with two primary tools:
    1. `save_note`: For general note-taking.
    2. `save_action_item`: For specific, actionable tasks.

    Your job is to listen to the user and decide which tool to use.

    - If the user's request is a general statement to be remembered,
      you MUST call the `save_note` tool.
      Example: "take a note that the budget is approved" -> call save_note(note="the budget is approved")

    - If the user's request contains phrases like "I will," "we need to,"
      "the next step is," or other clear indicators of a task, you MUST
      call the `save_action_item` tool.
      Example: "remember that we need to contact the vendor" -> call save_action_item(action_item="we need to contact the vendor")
      
    Always confirm which action you have taken.
    """,
    tools=[save_note, save_action_item]
)

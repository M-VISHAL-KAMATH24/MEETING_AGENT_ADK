import datetime
from google.adk.agents import Agent

# --- Step 1: Define the Custom Tool ---
# A tool is just a Python function. The ADK automatically understands
# the function name, its parameters, and its docstring.

def save_note(note: str) -> dict:
    """
    Saves a given text note to a file named 'meeting_notes.txt'.

    Args:
        note (str): The text content to be saved as a note.

    Returns:
        A dictionary confirming the status of the operation.
    """
    try:
        # We'll name the file based on the current date.
        filename = f"meeting_notes_{datetime.date.today()}.txt"
        
        # 'a' mode appends the note to the file if it exists,
        # or creates it if it doesn't.
        with open(filename, 'a') as f:
            f.write(f"- {note}\\n")
            
        print(f"DEBUG: Note '{note}' saved to {filename}") # For our own debugging
        
        # It's good practice for tools to return a status.
        return {"status": "success", "message": f"Note saved to {filename}."}
        
    except Exception as e:
        print(f"ERROR: Failed to save note. {e}")
        return {"status": "error", "message": str(e)}

# --- Step 2: Define the Agent ---
# We create a new agent and pass our new `save_note` function
# into the 'tools' list.

root_agent = Agent(
    name="note_taker_agent",
    model="gemini-2.0-flash",
    description="An agent that can save notes to a file.",
    instruction="""
    You are a helpful meeting assistant. Your primary function is to
    take notes when the user asks you to.
    
    When a user says something like "take a note", "save this", or
    "remember that", you must call the `save_note` tool.
    
    Pass the user's exact words as the 'note' parameter to the tool.
    After the tool is called, confirm to the user that the note has been saved.
    """,
    tools=[save_note] # Here's the magic!
)

# --- Step 3: Make the Agent Runnable ---
# The adk run command will look for this 'root_agent' variable.
# (No need for a __main__ block when using 'adk run')


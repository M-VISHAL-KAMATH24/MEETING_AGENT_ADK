import os
import base64
import datetime  # Import the datetime module
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.adk.agents import Agent

# --- Define Scopes and Paths (No Change) ---
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SCRIPT_DIR = os.path.dirname(__file__)
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token_gmail.json')

def send_follow_up_email(recipient: str, subject: str) -> dict:
    """
    Reads the meeting notes and action items, then sends them in a follow-up email.
    """
    # --- Part 1: Gather notes (THE CRITICAL FIX) ---
    try:
        # Get today's date in the same format used by the note-taker
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        
        # Dynamically create the filenames with today's date
        notes_filename = f"meeting_notes_{today_str}.txt"
        actions_filename = f"action_items_{today_str}.txt"

        notes_path = os.path.join(SCRIPT_DIR, '..', notes_filename)
        actions_path = os.path.join(SCRIPT_DIR, '..', actions_filename)

        email_body = "Hello,\n\nHere is a summary of our meeting.\n\n"
        
        email_body += "--- Meeting Notes ---\n"
        if os.path.exists(notes_path):
            with open(notes_path, 'r') as f:
                email_body += f.read()
        else:
            email_body += "No general notes were taken for today.\n"

        email_body += "\n--- Action Items ---\n"
        if os.path.exists(actions_path):
            with open(actions_path, 'r') as f:
                email_body += f.read()
        else:
            email_body += "No action items were identified for today.\n"
            
        email_body += "\nBest regards,\nYour AI Meeting Assistant"

    except Exception as e:
        return {"status": "error", "message": f"Failed to read note files: {str(e)}"}

    # --- Part 2: Authenticate and Send (No Change) ---
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        message = MIMEText(email_body)
        message["to"] = recipient
        message["subject"] = subject
        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        return {"status": "success", "message_id": send_message["id"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Define the Agent (No Change) ---
root_agent = Agent(
    name="email_agent",
    model="gemini-2.0-flash",
    description="An agent that can send a summary email of the meeting.",
    instruction="""
    You are a helpful assistant that sends follow-up emails.
    When the user asks you to send the meeting summary, you MUST use the `send_follow_up_email` tool.
    You will need to ask the user for the recipient's email address and the subject line.
    """,
    tools=[send_follow_up_email],
)

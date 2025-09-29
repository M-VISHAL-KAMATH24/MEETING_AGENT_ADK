import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.adk.agents import Agent

# --- Define Scopes ---
# We now request permission to SEND emails.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# --- Define absolute paths for credential files ---
SCRIPT_DIR = os.path.dirname(__file__)
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')
# We use a different token file to store the new permissions.
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token_gmail.json')

def send_follow_up_email(recipient: str, subject: str) -> dict:
    """
    Reads the meeting notes and action items, then sends them in a follow-up email.
    
    Args:
        recipient (str): The email address of the person to send the email to.
        subject (str): The subject line for the email.
        
    Returns:
        A dictionary confirming the status of the email sending operation.
    """
    # --- Part 1: Gather the notes and action items ---
    try:
        # Note: In a real app, these paths should be more robust or passed in.
        # For this example, we assume they are in the parent directory.
        notes_path = os.path.join(SCRIPT_DIR, '..', 'meeting_notes_2025-09-29.txt')
        actions_path = os.path.join(SCRIPT_DIR, '..', 'action_items_2025-09-29.txt')

        email_body = "Hello,\n\nHere is a summary of our meeting.\n\n"
        
        email_body += "--- Meeting Notes ---\n"
        if os.path.exists(notes_path):
            with open(notes_path, 'r') as f:
                email_body += f.read()
        else:
            email_body += "No general notes were taken.\n"

        email_body += "\n--- Action Items ---\n"
        if os.path.exists(actions_path):
            with open(actions_path, 'r') as f:
                email_body += f.read()
        else:
            email_body += "No action items were identified.\n"
            
        email_body += "\nBest regards,\nYour AI Meeting Assistant"

    except Exception as e:
        return {"status": "error", "message": f"Failed to read note files: {str(e)}"}

    # --- Part 2: Authenticate and Send the Email ---
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
        
        # Create the email message object
        message = MIMEText(email_body)
        message["to"] = recipient
        message["subject"] = subject
        
        # Encode the message in base64
        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
        
        # Call the Gmail API to send the message
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        return {"status": "success", "message_id": send_message["id"]}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Define the Agent ---
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

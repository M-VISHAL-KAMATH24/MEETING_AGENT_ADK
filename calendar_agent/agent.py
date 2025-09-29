import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.adk.agents import Agent

# --- Define Scopes (No Change) ---
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# --- THE CRITICAL FIX: Define absolute paths for credential files ---
# Get the directory where this python script is located.
SCRIPT_DIR = os.path.dirname(__file__)
# Create full paths to the credentials and token files.
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.json')


def get_upcoming_events() -> dict:
    """
    Connects to the Google Calendar API and retrieves the next upcoming events.
    """
    creds = None
    # Use the absolute path to check for and load the token.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the absolute path to load the client secrets file.
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials to the absolute path for the next run.
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=5,  # Changed from default argument
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return {"status": "success", "message": "No upcoming events found."}

        event_summaries = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_summaries.append(f"Event: {event['summary']} at {start}")
            
        return {"status": "success", "events": event_summaries}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Define the Agent (No Change) ---
root_agent = Agent(
    name="calendar_agent",
    model="gemini-2.0-flash",
    description="An agent that can read a user's Google Calendar.",
    instruction="""
    You are a helpful assistant with access to the user's Google Calendar.
    When the user asks about their schedule or upcoming meetings, you MUST use
    the `get_upcoming_events` tool to find the information.
    Summarize the events found in a clear, readable list for the user.
    """,
    tools=[get_upcoming_events],
)

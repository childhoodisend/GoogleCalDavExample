import os
from datetime import datetime, timezone, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth Settings
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials_example.json'


def get_authenticated_service():
    """Authenticate with Google Calendar API"""
    creds = None

    # Load existing credentials if available
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except ValueError as e:
            print(f"Error loading credentials: {e}")
            os.remove(TOKEN_FILE)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_FILE}. Get it from Google Cloud Console: "
                    "https://console.cloud.google.com/apis/credentials"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server()

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def main():
    print("Google Calendar - Last Week's Events")
    print("=" * 50)

    try:
        service = get_authenticated_service()

        now = datetime.now(timezone.utc)
        week_ago = now - timedelta(days=7)

        # (RFC3339 format)
        now_iso = now.isoformat()
        week_ago_iso = week_ago.isoformat()

        events_result = service.events().list(
            calendarId='primary',
            timeMin=week_ago_iso,
            timeMax=now_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            print("No events found in the last week.")
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event.get('summary', 'No title')

            print(f"{start} to {end}: {summary}")

    except Exception as e:
        print(f"Error {e}, see README.md")


if __name__ == '__main__':
    main()

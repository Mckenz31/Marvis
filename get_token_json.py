import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar"
]

def authorize_google():
    creds = None
    if os.path.exists( "token.json" ):
        creds = Credentials.from_authorized_user_file( "token.json" )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid or not creds.has_scopes( SCOPES ):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh( Request() )
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server( port = 8080 )
        # Save the credentials for the next run
        with open( "token.json", "w" ) as token:
            token.write( creds.to_json() )

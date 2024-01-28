from typing import Optional

from google.oauth2.credentials import Credentials
from llama_hub.tools.gmail import GmailToolSpec
from llama_hub.tools.google_calendar import GoogleCalendarToolSpec
from llama_index.tools.tool_spec.base import BaseToolSpec


class CustomGmailToolSpec( GmailToolSpec ):
    def __init__( self, user_file = None ):
        self.user_file = user_file

    def _get_credentials( self ):
        if self.user_file is None:
            return super()._get_credentials()
        return Credentials.from_authorized_user_info( self.user_file,
            [ "https://www.googleapis.com/auth/gmail.compose", "https://www.googleapis.com/auth/gmail.readonly" ]
        )

class CustomGoogleCalendarToolSpec( GoogleCalendarToolSpec ):
    def __init__( self, user_file = None ):
        self.user_file = user_file

    def _get_credentials( self ):
        if self.user_file is None:
            return super()._get_credentials()
        return Credentials.from_authorized_user_info( self.user_file,
     [ "https://www.googleapis.com/auth/calendar" ]
        )

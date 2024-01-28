import random
from datetime import datetime
from typing import Optional

from google.oauth2.credentials import Credentials
from llama_hub.tools.gmail import GmailToolSpec
from llama_hub.tools.google_calendar import GoogleCalendarToolSpec
from llama_index.tools import FunctionTool
from llama_index.tools.tool_spec.base import BaseToolSpec


class CustomGmailToolSpec( GmailToolSpec ):
    # spec_functions = [
    #     "load_data",
    #     "search_messages",
    #     "create_draft",
    #     "update_draft",
    #     "get_draft",
    #     "send_draft",
    # ]
    def __init__( self, user_file = None ):
        self.user_file = user_file
        self.spec_functions.remove( "load_data" )
        self.spec_functions.remove( "search_messages" )
        self.spec_functions.append( "search_email" )

    def search_email( self, query: str, max_results: Optional[ int ] = None ):
        """Searches the user's Gmail account using the specified query string."""
        return super().search_messages( query, max_results )

    def _get_credentials( self ):
        if self.user_file is None:
            return super()._get_credentials()
        return Credentials.from_authorized_user_info( self.user_file,
            [ "https://www.googleapis.com/auth/gmail.compose", "https://www.googleapis.com/auth/gmail.readonly" ]
        )

class CustomGoogleCalendarToolSpec( GoogleCalendarToolSpec ):
    # spec_functions = [ "load_data", "create_event", "get_date" ]

    def __init__( self, user_file = None ):
        self.user_file = user_file

    def _get_credentials( self ):
        if self.user_file is None:
            return super()._get_credentials()
        return Credentials.from_authorized_user_info( self.user_file,
     [ "https://www.googleapis.com/auth/calendar" ]
        )

transaction_history = [
    { "date": "1/27/24", "amount": "$5.64", "location": "McDonald's", "category": "fast food" },
    { "date": "1/26/24", "amount": "$32.46", "location": "Walmart", "category": "groceries" },
    { "date": "1/25/24", "amount": "$9.74", "location": "Chik-fil-A", "category": "fast food" },
    { "date": "1/25/24", "amount": "$16.98", "location": "Target", "category": "groceries" },
    { "date": "1/23/24", "amount": "$4.53", "location": "Starbucks", "category": "fast food" },
    { "date": "1/22/24", "amount": "$127.37", "location": "Best Buy", "category": "technology" },
]

weather = [ { "temp": "58", "condition": "sunny" } ] # [ { "temp": "72", "condition": "sunny" }, { "temp": "48", "condition": "snowy" }, { "temp": "80", "condition": "raining" } ]

def make_tool( fn, name, description ) -> FunctionTool:
    return FunctionTool.from_defaults( fn = fn, name = name, description = description )


date_tool = make_tool( lambda: datetime.now().strftime( "%d/%m/%Y" ), "date",
                       "Returns the current date in the format DD/MM/YYYY" )
time_tool = make_tool( lambda: datetime.now().strftime( "%H:%M" ), "time",
                       "Returns the current time in the format HH:MM" )
bank_tool = make_tool( lambda: transaction_history,
                       "bank", "Returns the user's transaction history" )
remember_tool = make_tool( lambda text = None: f"Okay, I saved this note for you: {text}", "remember",
                           "Saves a note on the user's device" )
reminder_tool = make_tool( lambda when = None, description = None: f"Okay, I set a reminder for {when}: {description}",
                           "set_reminder", "Sets an alarm on the user's device" )
play_music_tool = make_tool( lambda song = None: "Now streaming to Spotify.", "play_music",
                             "Searches for a song on Spotify and plays it on the user's device." )
set_setting_tool = make_tool( lambda setting_id = None, value = None: f"Set {setting_id} to {value}", "set_setting",
                              "Modifies a setting on the user's device." )
get_location_tool = make_tool( lambda: "College Station, TX", "get_location", "Returns the user's current location." )
get_weather_tool = make_tool( lambda location = None: random.choice( weather ), "get_weather", "Returns the user's current weather." )

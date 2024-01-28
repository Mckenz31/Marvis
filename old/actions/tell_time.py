from datetime import datetime

from old.util import speak


def tell_time():
    current_time = datetime.now().strftime( "%H:%M %p" )
    speak( f"The current time is {current_time}" )
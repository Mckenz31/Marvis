from datetime import datetime

from old.util import speak


def wish_me():
    hour = datetime.now().hour
    if 0 <= hour < 12:
        speak( "Good Morning!" )
    elif 12 <= hour < 18:
        speak( "Good Afternoon!" )
    else:
        speak( "Good Evening!" )

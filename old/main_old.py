from old.actions import summarize_wikipedia, tell_time, open_browser, search_google
from old.util import speak, listen

# pyttsx3
# wikipedia
# SpeechRecognition
# pyaudio

def callback():
    speak( "What can I do for you today?" )
    cmd = listen().lower()
    if "good bye" in cmd or "ok bye" in cmd or "turn off" in cmd:
        speak( "See you later!" )
        exit()
    elif "wikipedia" in cmd:
        summarize_wikipedia( cmd )
    elif "open google" in cmd:
        open_browser( "Google Chrome", "https://www.google.com" )
    elif "open youtube" in cmd:
        open_browser( "YouTube", "https://www.youtube.com" )
    elif "open gmail" in cmd:
        open_browser( "Gmail", "https://mail.google.com" )
    elif "search on google" in cmd:
        search_google()
    elif "what is the time" in cmd or "tell me the time" in cmd:
        tell_time()


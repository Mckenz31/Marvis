import webbrowser

from old.util import speak


def open_browser( website_name: str, url: str ):
    webbrowser.open_new_tab( url )
    speak( f"{website_name} is now open" )
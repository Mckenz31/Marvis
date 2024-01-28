import webbrowser

from old.util import speak, listen


def search_google():
    speak( "What do you want to search for?" )
    query = listen().lower()
    webbrowser.open_new_tab( f"https://www.google.com/search?q={query.replace( ' ', '+' )}" )
    speak( f"Searching Google for {query}" )
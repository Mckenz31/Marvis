from wikipedia import wikipedia

from old.util import speak


def summarize_wikipedia( query: str ):
    speak( "Searching Wikipedia" )
    results = wikipedia.summary( query, sentences = 3 )
    speak( "According to Wikipedia" )
    speak( results )
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init( 'sapi5' )


def speak( text ):
    engine.say( text )
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print( "Listening..." )
        audio = r.listen( source )

    try:
        statement = r.recognize_google( audio, language = 'en-in' )
        print( f"user said: {statement}\n" )

    except Exception as e:
        speak( "I didn't hear you, please say that again" )
        return None

    return statement


def load_api_keys():
    api_keys = {}
    with open( "api_keys.txt" ) as f:
        for line in f:
            name, value = line.partition( "=" )[ ::2 ]
            api_keys[ name.strip().upper() ] = value.strip()
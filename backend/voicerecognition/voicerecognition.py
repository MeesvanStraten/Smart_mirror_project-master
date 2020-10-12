import speech_recognition as sr
from backend.facerecognition.facerecognition import *
import os
from gtts import gTTS
import warnings
import random
import time
import webbrowser

warnings.filterwarnings('ignore')


# Record audio and return it as a string
def record_audio():
    # Record the audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source)

    # Speech recognition using Google's Speech Recognition
    data = ''
    try:
        data = r.recognize_google(audio, language="nl-NL")
        print('You said: ' + data)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand')
    except sr.RequestError as e:
        print('Request error from Google Speech Recognition')
    return data


# Function to get the virtual assistant response
def assistant_response(text):
    print(text)
    # Convert the text to speech
    myobj = gTTS(text=text, lang='nl', slow=False)

    # Save the converted audio to a file
    myobj.save('assistant_response.mp3')
    # Play the converted file
    os.system('start assistant_response.mp3')


def load():
    command_listen_to_name()

def command_listen_to_name():
    assisant_response = gTTS(text="wat is jouw name?", lang='nl', slow=False)
    assisant_response.save('assistant_response.mp3')
    os.system('start assistant_response.mp3')

    recorded_name = record_audio()
    recorded_name = gTTS(text=recorded_name, lang='nl', slow=False)
    recorded_name.save('assistant_response.mp3')
    os.system('start assistant_response.mp3')

    confirmation = gTTS(text="klopt deze naam?", lang='nl', slow=False)
    confirmation.save('assistant_response.mp3')
    os.system('start assistant_response.mp3')

    confirmation = record_audio()

    CONFIRMATION_WORDS = ['ja', 'dat klopt', 'dat is mijn naam']
    for phrase in CONFIRMATION_WORDS:
        if phrase in confirmation:
            return create_new_user(recorded_name.text)

    UNCONFIRMATION_WORDS = ['nee', 'dat is niet', 'dat is niet mijn naam', 'dat klopt niet']
    for phrase in UNCONFIRMATION_WORDS:
        if phrase in confirmation:
             return load()



# A function to check for wake word(s)
def wake_word(text):
    WAKE_WORDS = ['hi spiegel', 'hey spiegel', 'hallo spiegel', 'hay spiegel', 'oké spiegel']
    text = text.lower()  # Convert the text to all lower case words
    # Check to see if the users command/text contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    # If the wake word was not found return false
    return False


# Function to return a random greeting response
def greeting(text):
    # Greeting Inputs
    GREETING_INPUTS = ['hi', 'hey', 'hallo', 'hay', 'ok', 'oké']
    # Greeting Response back to the user
    GREETING_RESPONSES = ['howdy', 'Wie bende gij nou', 'hallo', 'Heey jij']
    # If the users input is a greeting, then return random response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    # If no greeting was detected then return an empty string
    return ''


def command_create_new_user(text):
    CREATE_USER_INPUTS = ['maak gebruiker']
    text = text.lower()
    for phrase in CREATE_USER_INPUTS:
        if phrase in text:
            command_listen_to_name()


def openBrowser(text):
    webbrowser.open("https://www.google.com/" + text)


timeout = 300


def assistant_listen():
    while True:
        # Record the audio
        text = record_audio()
        response = ''  # Empty response string
        # Checking for the wake word/phrase
        if (wake_word(text) == True):
            response = response + greeting(text)
            assistant_response(response)
            # sets the 300 second timer
            timeout_start = time.time()

            while time.time() < timeout_start + timeout:
                text = ''
                text = record_audio()
                text = text.lower()
                response = ''
                # Check for greetings by the user
                # Check to see if the user said date

                # if ('open' in text):
                #     openBrowser(text)

                command_create_new_user(text)

            print("not listing")

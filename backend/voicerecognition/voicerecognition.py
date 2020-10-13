import speech_recognition as sr
from backend.facerecognition.facerecognition import *
import os
from gtts import gTTS
import warnings
import random
import time
import webbrowser
from backend.voicerecognition.commandlibrary import *


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
    command_listen_to_name(True, True, )


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
    GREETING_RESPONSES = ['howdy', 'hallo', 'hi', 'Heey jij']
    # If the users input is a greeting, then return random response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    # If no greeting was detected then return an empty string
    return ''


def assistant_listen_response(confirm_user_input: bool, can_user_record: bool, response: str):
    user_input = ''
    if can_user_record:
        user_input = record_audio()
    recorded_name = gTTS(text=response, lang='nl', slow=False)
    recorded_name.save('assistant_response.mp3')
    if confirm_user_input:
        os.system('start assistant_response.mp3')
        if can_user_record:
            return user_input
    return ''


def command_listen_to_name(confirm_user_input: bool, can_user_record: bool):
    user_sentence = ""

    user_sentence = assistant_listen_response(confirm_user_input, can_user_record, response_name_confirmation[0])
    if user_sentence == '':
        user_sentence = assistant_listen_response(confirm_user_input, can_user_record, response_name_confirmation[0])

    user_confirmation = assistant_listen_response(confirm_user_input, can_user_record, "klopt dit?")
    for command in command_confirmation:
        if command in user_confirmation:
            return create_new_user(user_sentence)

    for request in request_change_confirmation:
        if request in user_sentence:
            return load()


def voice_command(user_sentence: str, commands: list):
    for command in commands:
        if user_sentence in command:
            print("command found")
            return True
        else:
            print("command not found")
            return False


def openBrowser(text):
    webbrowser.open("https://www.google.com/" + text)


timeout = 300


def assistant_listen():
    while True:
        # Record the audio
        user_sentence = record_audio()
        response = ''  # Empty response string
        # Checking for the wake word/phrase
        if (wake_word(user_sentence) == True):
            response = response + greeting(user_sentence)
            assistant_response(response)
            # sets the 300 second timer
            timeout_start = time.time()

            while time.time() < timeout_start + timeout:
                user_sentence = ''
                user_sentence = record_audio()
                user_sentence = user_sentence.lower()

                if voice_command(user_sentence=user_sentence, commands=command_make_new_user):
                    command_listen_to_name(True, True)

            print("not listing")


response = ["doet die het", "werkt het"]

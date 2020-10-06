import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import random
import wikipedia
import time

warnings.filterwarnings('ignore')


# Record audio and return it as a string
def recordAudio():
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
def assistantResponse(text):
    print(text)
    # Convert the text to speech
    myobj = gTTS(text=text, lang='nl', slow=False)

    # Save the converted audio to a file
    myobj.save('assistant_response.mp3')
    # Play the converted file
    os.system('start assistant_response.mp3')


# A function to check for wake word(s)
def wakeWord(text):
    WAKE_WORDS = ['hallo', 'oke computer']
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
    GREETING_INPUTS = ['hi', 'hey', 'hola', 'wassup', 'hallo']
    # Greeting Response back to the user
    GREETING_RESPONSES = ['howdy', 'Wie bende gij nou', 'hallo', 'Heey jij']
    # If the users input is a greeting, then return random response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    # If no greeting was detected then return an empty string
    return ''

# Function to get a person first and last name
def getPerson(text):
 wordList = text.split()# Split the text into a list of words
 for i in range(0, len(wordList)):
   if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

timeout = 30

while True:
    # Record the audio
    text = recordAudio()
    response = ''  # Empty response string
    # Checking for the wake word/phrase
    if (wakeWord(text) == True):
        response = response + greeting(text)
        assistantResponse(response)
        # sets the 300 second timer
        timeout_start = time.time()

        while time.time() < timeout_start + timeout:
            text = recordAudio()
            # Check for greetings by the user
            # Check to see if the user said date
            if ('tijd' in text):
                now = datetime.datetime.now()
                meridiem = ''
                if now.hour >= 12:
                    meridiem = 'p.m'  # Post Meridiem (PM)
                    hour = now.hour - 12
                else:
                    meridiem = 'a.m'  # Ante Meridiem (AM)
                    hour = now.hour
                    # Convert minute into a proper string
                if now.minute < 10:
                    minute = '0' + str(now.minute)
                else:
                    minute = str(now.minute)
                response = response + ' ' + 'Het is ' + str(hour) + ':' + minute + '.'
                assistantResponse(response)
                timeout = timeout + timeout
        print("not listing")

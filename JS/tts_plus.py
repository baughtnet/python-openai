import os
import openai
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS

# Import the OpenAI API key from an environment variable OPENAI_API
openai_api_key = os.environ.get('OPENAI_API')

# Start listening on the microphone for the keyword "help please"
# Will wait indefinitely for the keyword

def start_listening():
    # Create a recognizer object
    r = sr.Recognizer()

    # Start listening on the microphone
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust microphone for ambient noise
        r.adjust_for_ambient_noise(source)

        # Listen for the keyword "help please"
        audio = r.listen(source, phrase_time_limit=None)

        

        try:
            # Convert speech to text
            text = r.recognize_google(audio)

            # Check if the keyword "help please" is detected
            if "help please" in text.lower():
                print("Keyword detected!")
                # Perform actions when the keyword is detected
                success_txt = "How can I help you?"
                text_to_speech(success_txt)
                take_voice_input()

        except sr.UnknownValueError:
            print("Sorry, I did not understand what you said.")
        except sr.RequestError as e:
            print("Sorry, I am unable to process your request. Please try again later.")

# function to send text to chatgpt
def send_to_chatgpt(text):
    openai.api_key = openai_api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    results = completion.choices[0].message.content
    results_text = "Based on a variety of online sources, I have found the following information:"
    text_to_speech(results_text)
    text_to_speech(results)

# function to take voice input and covert it to text
def take_voice_input():
    # Create a recognizer object
    r = sr.Recognizer()

    # Start listening on the microphone
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            # Convert speech to text
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
            lookup_text = "Just give me a moment to look that up for you."
            text_to_speech(lookup_text)
            send_to_chatgpt(text)

        except sr.UnknownValueError:
            print("Sorry, I did not understand what you said.")
            err1 = "Sorry, I did not understand what you said."
            text_to_speech(err1)
        except sr.RequestError as e:
            print("Sorry, I am unable to process your request. Please try again later.")


# function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")

# Call the function to start listening
start_listening()

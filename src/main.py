import pathlib
import textwrap

from google import genai

import signal
from elevenlabs.client import ElevenLabs
from elevenlabs import voices
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs import play

import textwrap
import speech_recognition as speech_rec

def to_markdown(text):
    text = text.replace('•', '  *')
    formatted_text = textwrap.indent(text, '> ', predicate=lambda _: True)
    print(formatted_text)

# Used to securely store your API key
from privateData import API_KEY, ElevenLabsAgentID, ElevenLabsVoiceID, ElevenLabsAPIKey, ffmpegPath
import os

os.environ['PATH'] += os.pathsep + ffmpegPath

# GOOGLE IMPLEMENTATION
#CONFIGURE OUR AI
my_model = "gemini-2.0-flash"

client = genai.Client(api_key=API_KEY)
chat = client.chats.create(model=my_model)

#SPEECH RECOGNITION SETUP
recognizer = speech_rec.Recognizer()
recognizer.pause_threshold = 2.0
recognizer.energy_threshold = 500

def listen_for_audio() -> str:
    # Use the default microphone as the audio source
    with speech_rec.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            said_text = recognizer.recognize_google(audio)
            print("You said: ", said_text)
            return said_text

        except speech_rec.UnknownValueError:
            print("Sorry, could not understand the audio.")
            return None
        except speech_rec.RequestError:
            print("Could not request results; check your internet connection.")
            return None

#ELEVENLABS SETUP
elevenlabs = ElevenLabs(api_key=ElevenLabsAPIKey)

def speak_text(_text):
    audio = elevenlabs.text_to_speech.convert(
        text=_text,
        voice_id=ElevenLabsVoiceID,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)


#Function Prompt our AI
def prompt_ai():
  fullResponse = ""
  keep_talking = True

  while keep_talking:
    user_prompt = listen_for_audio() #input("\nPrompt: \n") #Ask the user to say something

    if(user_prompt == None):
        print("Sorry, I didn't catch that, please try again")
        continue


    if user_prompt != "exit": #If they didn't say exit, send their message to our chatbot

      response = chat.send_message_stream(user_prompt)

      print("\nJOYCE: ")

      for chunk in response: #Get the response
        #print(chunk.text)
        fullResponse += chunk.text

      print("FULL RESP: " + fullResponse)
      speak_text(fullResponse)
      fullResponse = ''


    else: # Otherwise, they said exit, so leave
      keep_talking = False


prompt_ai()


#DEBUGGING SPEECH LISTENER
'''
print("Please say something...")
listen_for_audio()
'''



'''def get_voices():
    response = elevenlabs.voices.get_all()
    print(response.voices)
'''
#CODE FOR USING THEIR AGENT/LLM
'''conversation = Conversation(
    # API client and agent ID.
    elevenlabs,
    ElevenLabsVoiceKey,
    # Assume auth is required when API_KEY is set.
    requires_auth=bool(ElevenLabsAPIKey),
    # Use the default audio interface.
    audio_interface=DefaultAudioInterface(),
    # Simple callbacks that print the conversation to the console.
    callback_agent_response=lambda response: print(f"JOYCE: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"JOYCE: {original} -> {corrected}"),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),
    # Uncomment if you want to see latency measurements.
    # callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),
)

conversation.start_session()

#cleanup. End the convo when we're done
signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

#print the transcript
conversation_id = conversation.wait_for_session_end()
print(f"Conversation ID: {conversation_id}")
'''
#get_voices()
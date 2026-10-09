import discord
from discord.ext import commands
import pyttsx3
from TOKEN import token
import sounddevice as sd
import speech_recognition as sr
import scipy.io.wavfile as wav
from googletrans import Translator
import requests
import json

engine = pyttsx3.init()
engine.setProperty('rate', 135)

duration = 5
sample_rate = 44100


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} Entered.")


@bot.command()
async def talk(ctx):
    text = "Imagine Earth is wearing a heavy blanket of pollution " \
       "that it cannot take off. " \
       "This is global warming, and it is changing our lives " \
       "in surprising ways. " \
       "First, your coffee and chocolate are in danger because " \
       "heat waves are ruining crops. " \
       "Second, the ocean is a giant sponge, absorbing ninety " \
       "percent of our extra heat. " \
       "Third, time is actually slowing down as melting ice " \
       "shifts the planet's weight and slowing down its rotation. " \
       "Fourth, zombie bacteria are waking up from melting " \
       "frozen ground. " \
       "The good news? We can take this blanket off by saving " \
       "energy today."
    engine.say(f'Hello, I am the hackathon bot and I will be talking about the\
                global warming and its affects on people and other creatures \
                lives...,{text}'
               )
    engine.runAndWait()
    engine.say("What is your idea about global warming? do you think it is\
        dangerous to human and other species' environment?")
    engine.runAndWait()
    recording = sd.rec(
        int(duration*sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16")
    sd.wait()

    wav.write("output.wav", sample_rate, recording)
    print("recording stopped, translating")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en").lower()
        print("processing")

    except sr.UnknownValueError:    # - Is caused by the volume of your sound
        print("Konuşma tanınamadı.")
    except sr.RequestError as e:        # - Is caused by internet or API
        print(f"Hizmet hatası: {e}")

    if text == "yes":

        base_url = 'https://global-warming.org/api/temperature-api'
        response = requests.get(base_url)
        if response.status_code == 200:
            response = json.dumps(response.text.strip)

            good = f'very well, that shows that you believe in \
                global warming. But if i told you that. {response}'
            engine.say(good)
            engine.runAndWait

        else:
            engine.say("Sorry, the image could not be accessed, please retry")
            engine.runAndWait


bot.run(token)

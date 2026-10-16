import discord
from discord.ext import commands
import pyttsx3
from TOKEN import token
import sounddevice as sd
import speech_recognition as sr
import scipy.io.wavfile as wav
import requests


engine = pyttsx3.init()
engine.setProperty("rate", 135)

duration = 5
sample_rate = 44100

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.command()
async def talk(ctx):
    introduction = (
        "Hello everyone! Today we will talk about global warming. "
        "Global warming is the long-term increase in Earth's "
        "average temperature. Human activities are a major cause. "
        "Would you like to learn a fact about global warming? "
        "Please say yes or no."
    )

    engine.say(introduction)
    engine.runAndWait()

    print("Listening for 5 seconds...")

    try:
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()

        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        recognized_text = recognizer.recognize_google(
            audio, language="en-US"
        ).lower()

        print("You said:", recognized_text)

    except sr.UnknownValueError:
        engine.say("Sorry, I could not understand your answer.")
        engine.runAndWait()
        return

    except sr.RequestError as error:
        print("Speech recognition error:", error)
        engine.say("Speech recognition is unavailable.")
        engine.runAndWait()
        return

    except Exception as error:
        print("Microphone error:", error)
        engine.say("I could not record your voice.")
        engine.runAndWait()
        return

    if "yes" in recognized_text.split():
        api_url = "https://global-warming.org/api/temperature-api"

        try:
            api_response = requests.get(api_url, timeout=15)
            api_response.raise_for_status()

            data = api_response.json()
            results = data.get("result", [])

            if not results:
                engine.say("No temperature data was found.")
                engine.runAndWait()
                return

            fact = (
                "Here is a climate fact. In 2016, "
                "the recorded temperature anomaly was "
                "54 degrees Celsius "
                "relative to the dataset's reference baseline. "
                "This is a temperature difference, "
                "not Earth's absolute temperature."
            )

            await ctx.send(fact)
            engine.say(fact)
            engine.runAndWait()

            await ctx.send("I read a climate fact aloud!")

        except (requests.RequestException, ValueError, KeyError) as error:
            print("API error:", error)
            engine.say("Sorry, I could not retrieve the climate data.")
            engine.runAndWait()

    else:
        engine.say("Thank you for sharing your opinion!")
        engine.runAndWait()


bot.run(token)

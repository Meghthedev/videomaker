import openai
import requests
import random
from gtts import gTTS
import cv2
from pydub import AudioSegment
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip

def generate_quote():
    # Read the OpenAI API key from a file
    with open("api_key.txt", "r") as f:
        api_key = f.read().strip()

    # Set the OpenAI API key
    openai.api_key = api_key

    # Define the prompt to generate a motivational quote from Bhagwad Geeta
    prompt = (
        "Generate a motivational quote 2 to 3 lines long but do not leave new line or spaces between each line."
    )

    # Set the parameters for the GPT-3 model
    model = "text-davinci-002"
    temperature = 0.5
    max_tokens = 50

    # Generate the quote using the GPT-3 API
    response = openai.Completion.create(
    engine=model, prompt=prompt, temperature=temperature, max_tokens=max_tokens
    )

    # Extract the generated quote from the response
    quote = response.choices[0].text.strip()

    quote = quote.replace('"', '')

    # Save the quote to a file named quote.txt
    with open("quote.txt", "w") as f:
        f.write(quote)

def fetch_vid():
    # Enter Pixabay api key here
    key = ""
    query_params = {
    "key": key,
    "q": "nature",
    "orientation": "vertical",
    "video_type": "film"
    }

    # Send the request and get the response
    response = requests.get("https://pixabay.com/api/videos/", params=query_params)
    
    # Get a random video from the response
    video_data = response.json()["hits"][random.randint(0, len(response.json()["hits"])-1)]
    video_url = video_data["videos"]["large"]["url"]

    # Download the video and save it locally as "video.mp4"
    video_response = requests.get(video_url)
    with open("video.mp4", "wb") as f:
        f.write(video_response.content)

def generate_audio():
    with open("quote.txt", "r") as file:
        text = file.read()

    # Set language to English and Indian accent
    language = 'en-in'

    # Create a gTTS object and generate audio
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")

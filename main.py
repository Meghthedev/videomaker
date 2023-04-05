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

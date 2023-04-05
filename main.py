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

def cut_vid():
    audio_path = 'output.mp3'
    video_path = 'video.mp4'
    output_path = 'cutvideo.mp4'

    # Load audio and get its duration
    audio = AudioSegment.from_file(audio_path)
    audio_duration = audio.duration_seconds * 1000

    # Load video and get its duration
    cap = cv2.VideoCapture(video_path)
    video_duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) * 1000)

    # If the video is longer than the audio, cut the video to match the audio duration
    if video_duration > audio_duration:
        cap.set(cv2.CAP_PROP_POS_MSEC, 0)
        end_frame = int(audio_duration / 1000 * cap.get(cv2.CAP_PROP_FPS))
    else:
        end_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Write the new video to file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == end_frame:
                break
        else:
            break
    cap.release()
    out.release()

def caption():
    # Load audio and get its duration
    audio_path = 'output.mp3'
    video_path = 'cutvideo.mp4'
    text_path = 'quote.txt'

    # Load the audio file
    audio_clip = AudioFileClip(audio_path)

    # Load the text from the file
    with open("quote.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    # Define the output video file
    out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc(*'mp4v'), audio_clip.fps, (1920,1080))

    # Set the font and the font size for the captions
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    font_thickness = 2

    # Set the initial timestamp
    current_time = 0

    # Process each line of text and add the caption to the video
    for line in lines:
        # Get the duration of the current line
        duration = len(line) / 10

        # Get the end time of the current line
        end_time = current_time + duration

        # Generate the caption image
        caption_img = generate_caption_image(line, font, font_size, font_thickness)

        # Add the caption to the video for the duration of the current line
        while current_time < end_time:
            # Get the current frame
            frame = get_frame(current_time)

            # Add the caption to the frame
            frame = add_caption_to_frame(frame, caption_img)

            # Write the frame to the output video
            out.write(frame)

            # Increment the current time
            current_time += 1 / audio_clip.fps

    # Release the video writer
    out.release()

    # Close the audio file
    audio_clip.close()
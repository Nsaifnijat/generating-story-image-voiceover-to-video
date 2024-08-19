from openai import OpenAI
import credentials
import asyncio
from pathlib import Path
import requests

client = OpenAI(api_key=credentials.open_ai_key)

# Define the asynchronous function to call the API
def text_to_speech(text, voice, model, speech_title, filetype):
    try:
        # Generate speech audio
        response = client.audio.speech.create(
            model=model,
            voice=voice,  # speaker model
            input=text,
        )

        # Save the audio file
        audio_folder = Path('media/voice_over/')
        audio_folder.mkdir(parents=True, exist_ok=True)
        final_audio_path = audio_folder / f"{speech_title}_speech.{filetype}"
        response.stream_to_file(final_audio_path)

        return final_audio_path
    except Exception as e:
        return str(e)



def text_to_image(model, prompt, img_size, img_quality, img_name):

    response = client.images.generate(
    model=model,
    prompt=prompt,
    size=img_size,
    quality=img_quality,
    n=1,
    )

    image_url = response.data[0].url


    # Download the image and save it locally
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(f"media/images/{img_name}.png", "wb") as f:
            f.write(image_response.content)
        print("Image saved successfully!")
    else:
        print("Failed to retrieve the image.")


"""
# Ensure your API key is set as an environment variable
if not os.getenv("OPENAI_API_KEY"):
    print("Please set your OPENAI_API_KEY as an environment variable.")
    exit(1)
"""
def text_generation(conversation, model):
    try:
        response = client.chat.completions.create(
            model = model,  # You can change this to "gpt-4" if you have access
            messages = conversation
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"




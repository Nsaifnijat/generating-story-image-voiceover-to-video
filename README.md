# automatic-story-image-voiceover-generation-to-video
# StoryForge AI

StoryForge AI is an automated content creation and distribution pipeline that leverages OpenAI's GPT models to generate engaging stories, convert them to speech, create accompanying images, produce videos, and share them on popular social media platforms.

## Features

- Story Generation: Creates unique stories using OpenAI's language models
- Text-to-Speech Conversion: Transforms written stories into spoken narratives
- Image Creation: Generates images based on the story content
- Video Production: Combines narrated audio, story text, and images into engaging video content
- Multi-Platform Distribution: Automatically shares content on Instagram and Telegram

## Dependencies

This project relies on the following Python libraries:

```
moviepy
numpy
Pillow
openai
instagrapi
telethon
requests

```

## Setup

1. Clone this repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up your API credentials in a `credentials.py` file (see Configuration section)

## Configuration

Create a `credentials.py` file with the following structure:

```python
OPENAI_API_KEY = "your_openai_api_key"
INSTAGRAM_USERNAME = "your_instagram_username"
INSTAGRAM_PASSWORD = "your_instagram_password"
TELEGRAM_API_ID = "your_telegram_api_id"
TELEGRAM_API_HASH = "your_telegram_api_hash"
TELEGRAM_PHONE_NUMBER = "your_telegram_phone_number"
# Add any TTS-specific credentials if needed
```

## Usage

Run the main script to start the content creation and distribution process:

```
python create_reels.py
```

## How it Works

1. Story Generation: Uses OpenAI's GPT model to create a unique story
2. Text-to-Speech: Converts the written story into spoken audio
3. Image Creation: Generates an image related to the story using AI
4. Video Production: Combines the narrated audio, story text, and image into a video
5. Social Media Distribution: Uploads the video to Instagram and sends it via Telegram

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


from reel_functions import create_instagram_reel
from llm_functions import *
from llm_settings import *
import json
from socials import *
from credentials import *
from reel_config import config


print('creating a story')
response = text_generation(conversation, text_model)
with open('response.txt','w') as f:
    f.write(response)
print('story created!')


print('loading the story and image prompts from file!')
# Read the file
with open('response.txt', 'r') as file:
    json_string = file.read()
    data = json.loads(json_string)
    
voice_over_text = data['story']
img_1 = data['img_prompt_1']
img_2 = data['img_prompt_2']
video_caption = data['caption']
video_hashtags = data['hashtags']
video_bgmusic = data['background_music']

print('creating images')
text_to_image(img_model, img_1, img_size, img_quality, f'{img_name}_1')
text_to_image(img_model, img_2, img_size, img_quality, f'{img_name}_2')

#creating audio
audio_files = text_to_speech(voice_over_text, voice_type, voice_model, voice_name, 'mp3')
print('audio successfully created!')


if __name__ == "__main__":
    #creating video
    reel = create_instagram_reel(config, voice_over_text)
    reel.write_videofile(config['output_path'], fps=config['video_fps'], codec='libx264', audio_codec='aac')
        
    reel_path = config['output_path']
    reel_caption = video_caption
    reel_hashtags = video_hashtags
    tg_target_group = "kkkkkk" # put your telegram group that you want to upload the videos to.
    #uploading to telegram group
    send_video(tg_phone, tg_api_id, tg_api_hash, tg_target_group, reel_path, reel_caption)
    #uploading to instagram
    uploaded_reel = upload_reel(reel_path, reel_caption, reel_hashtags)

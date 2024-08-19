from instagrapi import Client
import time
import random
import credentials
from telethon import TelegramClient
import asyncio


# Login
client = Client()
client.login(credentials.instagram_username, credentials.instagram_password)
#print(client.user_id)
#print(help(client))

user_id = client.user_id
#my_own_posts = client.user_medias(user_id, 5)


def upload_picture(image_path, caption, hashtags):
    full_caption = f"{caption}\n\n{' '.join(hashtags)}"
    media = client.photo_upload(image_path, caption=full_caption)
    print(f"Uploaded picture: {media.pk}")
    return media

def upload_reel(video_path, caption, hashtags):
    full_caption = f"{caption}\n\n{' '.join(hashtags)}"
    media = client.clip_upload(video_path, caption=full_caption)
    print(f"Uploaded reel: {media.pk}")
    return media

def upload_post(image_paths, caption, hashtags):
    full_caption = f"{caption}\n\n{' '.join(hashtags)}"
    media = client.album_upload(image_paths, caption=full_caption)
    print(f"Uploaded post: {media.pk}")
    return media



async def send_telegram_video(phone, api_id, api_hash, target_group, video_path, caption=""):
    client = TelegramClient(phone, api_id, api_hash)
    
    try:
        await client.connect()
        
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))

        print(f"Sending video to {target_group}...")
        await client.send_file(target_group, video_path, caption=caption)
        print("Video sent successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        await client.disconnect()

def send_video(phone, api_id, api_hash, target_group, video_path, caption=""):
    asyncio.run(send_telegram_video(phone, api_id, api_hash, target_group, video_path, caption))




"""

# Upload a picture
picture_path = "media/images/iceland.jpg"
picture_caption = "Check out this amazing view!"
picture_hashtags = ["#nature", "#photography", "#instagram"]
uploaded_picture = upload_picture(picture_path, picture_caption, picture_hashtags)

# Wait a bit before next upload
time.sleep(random.randint(30, 60))

# Upload a reel
reel_path = "reels11.mp4"
reel_caption = "New dance move! What do you think?"
reel_hashtags = ["#dance", "#reels", "#fun"]
#uploaded_reel = upload_reel(reel_path, reel_caption, reel_hashtags)

# Wait a bit before next upload
time.sleep(random.randint(30, 60))

# Upload a post with multiple images
post_image_paths = [
    "media/images/brazil.jpg",
    "media/images/new_zealand.jpg"
]
post_caption = "A day in the life! Swipe to see more."
post_hashtags = ["#lifestyle", "#photodump", "#instagram"]
uploaded_post = upload_post(post_image_paths, post_caption, post_hashtags)"""
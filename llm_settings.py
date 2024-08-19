#role: system --- you set the behavior of the model
#role: user ---> you ask your question
#role: assitant --> you put the response of the model here, so you just attach to this role in order to have more context. optional
text_model = "gpt-4o-mini" #"gpt-3.5-turbo" , "gpt-4o" 
text_model_behavior = """You are a professional and highly skilled content creator who especializes in depicting interesting and educating real stories 
from ancient history or current to the viewers. You write engaging, one minutes stories that teach people a great life lesson without telling them the lesson,
its the story which teaches them. you return a result as a dict, that have the story, two very descriptive prompts that create awesome and high quality image that are
perfectly depicting that story, the prompts should always be two prompts that create two images that are completely a depiction of the story itself and
be very descriptive about images created for that story, they should create every part of the image everything according to the story figures and don't mess the era too,
a great caption, 7 hashtags that can increase the reach of the video, and what background music 
should be used for that story. keys for the returned dictionary are story, img_prompt_1, img_prompt_2, caption, hashtags, and background_music."""
text_prompt = """give me a real story from civil war which is catchy and really teaching people some fact of life. 
and elaborate it in a way that can be put into an engaging story narration for listeners, it should tell a fascinating one minute story with great wisdoms in it. Just
bring up the story in away that the listener learns the lesson from the story, you don't tell them what to learn. return to me a dict with story, image prompt for that story, 
"""
system_response = "Its Washington DC."
conversation = [
        {"role": "system", "content": text_model_behavior },
        {"role": "user", "content": text_prompt},
        #{"role": "assistant", "content": system_response} 
    ]


img_model="dall-e-3"
img_prompt="create image of a hazara young boy, holding afghanistan flag and a gun while on top of rocky mountains"
img_size="1024x1024"
img_quality="hd"
img_name = 'hazara'


voice_text = None
voice_type = 'alloy'
voice_name = 'saif'
voice_model = "tts-1"







from moviepy.editor import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap
import random

def create_title_clip(text, duration, width, height, font, font_size, bg_color, text_color):
    clip = ColorClip(size=(width, height), color=bg_color)
    txt_clip = TextClip(text, fontsize=font_size, color=text_color, font=font)
    txt_clip = txt_clip.set_position('center').set_duration(duration)
    return CompositeVideoClip([clip, txt_clip]).set_duration(duration)

def create_image_clip(image_path, duration, width, height, pan_direction, apply_saturation, saturation_start, 
                      saturation_end, apply_shaky, shake_intensity, shake_duration, shake_count):
    img = Image.open(image_path)
    img_width = int(img.width * height / img.height)
    img = img.resize((max(img_width, width * 2), height), Image.LANCZOS)
    
    shake_times = [random.uniform(0, duration - shake_duration) for _ in range(shake_count)]
    shake_times.sort()
    
    def make_frame(t):
        progress = t / duration
        if pan_direction == 'left_to_right':
            left_position = int(progress * (img.width - width))
        else:  # right_to_left
            left_position = int((1 - progress) * (img.width - width))
        top_position = 0
        
        if apply_shaky:
            for shake_start in shake_times:
                if shake_start <= t < shake_start + shake_duration:
                    shake_progress = (t - shake_start) / shake_duration
                    shake_amount = int(np.sin(shake_progress * np.pi) * shake_intensity)
                    left_position += shake_amount
                    top_position += random.randint(-shake_amount, shake_amount)
                    break
        
        cropped = img.crop((left_position, top_position, left_position + width, top_position + height))
        
        if apply_saturation:
            saturation_factor = saturation_start + (saturation_end - saturation_start) * progress
            enhancer = ImageEnhance.Color(cropped)
            cropped = enhancer.enhance(saturation_factor)
        
        return np.array(cropped)
    
    return VideoClip(make_frame, duration=duration)

def create_subtitle_mask(text, duration, width, height, font, font_size, max_chars_per_line, 
                         lines_to_show, bottom_margin, line_spacing, bg_color, text_color, 
                         highlight_color, highlight_text_color):
    words = text.split()
    total_words = len(words)

    def make_frame(t):
        # Determine progress and current text to display
        progress = t / duration
        word_count = max(1, int(total_words * progress))
        current_text = ' '.join(words[:word_count])
        
        # Create a blank image
        img = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        font_obj = ImageFont.truetype(font, font_size)
        
        # Wrap text to fit within the maximum character limit per line
        lines = textwrap.wrap(current_text, width=max_chars_per_line)
        
        # Set a fixed y-position to keep the subtitles at the bottom
        y_text = height - (lines_to_show * (font_size + line_spacing)) - bottom_margin
        
        total_words_displayed = 0
        for line in lines[-lines_to_show:]:
            words_in_line = line.split()
            bbox = draw.textbbox((0, 0), line, font=font_obj)
            text_width = bbox[2] - bbox[0]
            x_text = (width - text_width) // 2
            
            # Draw background rectangle for the whole line
            draw.rectangle([x_text-5, y_text, x_text+text_width+5, y_text+font_size+10], fill=bg_color)
            
            for i, word in enumerate(words_in_line):
                word_width = draw.textlength(word, font=font_obj)
                total_words_displayed += 1
                
                # Highlight the current word based on overall progress
                if total_words_displayed == word_count:
                    draw.rectangle([x_text-5, y_text, x_text+word_width+5, y_text+font_size+10], 
                                   fill=highlight_color)
                    draw.text((x_text, y_text), word, font=font_obj, fill=highlight_text_color)
                else:
                    draw.text((x_text, y_text), word, font=font_obj, fill=text_color)
                
                x_text += word_width + draw.textlength(" ", font=font_obj)
            
            y_text += font_size + line_spacing  # Move to the next line (stays at bottom)

        return np.array(img)
    
    return VideoClip(make_frame, duration=duration).to_mask()

def create_instagram_reel(config, subtitle_text):
    
    voiceover_audio = AudioFileClip(config['voiceover_path'][-1])
    clips = []
    total_duration = voiceover_audio.duration #config['duration']
    start_time = 0
    
    # Create title clip if specified
    if config.get('title'):
        title_clip = create_title_clip(config['title'], config['title_duration'], config['width'], config['height'], 
                                       config['font'], config['title_font_size'], config['title_bg_color'], 
                                       config['title_text_color'])
        clips.append(title_clip)
        start_time += config['title_duration']
        total_duration -= config['title_duration']
    
    # Calculate image duration
    image_duration = total_duration / len(config['image_paths'])
    
    # Create image clips
    for i, img in enumerate(config['image_paths']):
        pan_direction = 'left_to_right' if i % 2 == 0 else 'right_to_left'
        clip = create_image_clip(img, image_duration, config['width'], config['height'], pan_direction, 
                                 config['apply_saturation'], config['saturation_start'], config['saturation_end'], 
                                 config['apply_shaky'], config['shake_intensity'], config['shake_duration'], 
                                 config['shake_count'])
        clip = clip.set_start(start_time + i*image_duration)
        clips.append(clip)
    
    # Create subtitle clip
    subtitle_mask = create_subtitle_mask(subtitle_text, total_duration, 
                                         config['width'], config['height'], config['font'], config['subtitle_font_size'], 
                                         config['max_chars_per_line'], config['subtitle_lines_to_show'], 
                                         config['subtitle_bottom_margin'], config['subtitle_line_spacing'], 
                                         config['subtitle_bg_color'], config['subtitle_text_color'], 
                                         config['highlight_color'], config['highlight_text_color'])
    subtitle_clip = ColorClip(size=(config['width'], config['height']), color=(255, 255, 255))
    subtitle_clip = subtitle_clip.set_mask(subtitle_mask)
    subtitle_clip = subtitle_clip.set_opacity(config['subtitle_opacity']).set_start(start_time)
    clips.append(subtitle_clip)
    
    # Compose video
    video = CompositeVideoClip(clips)
    
    # Add audio
    bg_music = AudioFileClip(config['bg_music_path']).volumex(config['bg_music_volume'])
    bg_music = bg_music.set_duration(total_duration)
    audio = CompositeAudioClip([voiceover_audio, bg_music])
    final_video = video.set_audio(audio)
    
    final_video = final_video.set_duration(total_duration)
    return final_video
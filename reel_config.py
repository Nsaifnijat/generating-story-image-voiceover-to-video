import os
from pathlib import Path

def get_files_in_directory(directory):
    # Define allowed file extensions for each media type
    audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.aac'}
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
    
    allowed_extensions = audio_extensions.union(image_extensions, video_extensions)
    
    media_files = []
    
    try:
        for file in os.listdir(directory):
            file_path = Path(directory) / file
            if file_path.is_file() and file_path.suffix.lower() in allowed_extensions:
                media_files.append(str(file_path))
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
    
    return media_files
config = {
    # Video dimensions
    'width': 1080,
    'height': 1920,
    
    # Fonts
    'font': 'Arial',
    'subtitle_font_size': 50,
    'title_font_size': 70,
    
    # Durations
    'duration': 15,
    'title_duration': 3,  # Only used if title is provided
    
    # Subtitle settings
    'max_chars_per_line': 40,
    'subtitle_lines_to_show': 2,
    'subtitle_bottom_margin': 50,
    'subtitle_line_spacing': 10,
    
    # Colors
    'subtitle_bg_color': (128, 128, 128),
    'subtitle_text_color': (255, 255, 255),
    'highlight_color': (255, 255, 0),
    'highlight_text_color': 'black',
    'title_bg_color': (25, 25, 112),
    'title_text_color': 'white',
    
    # Opacity
    'subtitle_opacity': 1,
    
    # Audio settings
    'bg_music_volume': 0.05,
    
    # Video settings
    'video_fps': 30,
    
    # Saturation settings
    'apply_saturation': True,
    'saturation_start': 1,
    'saturation_end': 1.8,
    
    # Shaky effect settings
    'apply_shaky': True,
    'shake_intensity': 10,
    'shake_duration': 0.5,
    'shake_count': 2,
    
    # File paths
    'image_paths': get_files_in_directory('media/images'),
    'voiceover_path': get_files_in_directory('media/voice_over'),
    'bg_music_path': 'media/background_music/background.mp3',
    'output_path': 'media/output/reels9.mp4',
    
    # Content
    'title': None, #"Amazing Travel Destinations",  # Set to None or remove this line to skip title
    'subtitle_text': "This is a sample subtitle text that will be displayed over the video. It demonstrates the typing effect.",
}
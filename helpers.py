from moviepy.editor import AudioFileClip
from datetime import datetime
import re


def format_title_string(title):
    # Remove any special characters in the title string leaving only alphanumeric and spaces
    formatted_title = re.sub(r'[^\w ]', '', title)
    return formatted_title


def format_date_string(result):
    # Format date string to DD-MM-YYYY, HH:MM:SS format
    date_fetched = result[0].text_content()
    date_stripped = date_fetched[20:-10] + date_fetched[-8:-2]
    date = datetime.strptime(date_stripped, '%H:%M %Z on %B %d, %Y').strftime('%d-%m-%Y %H:%M:%S')
    return date


def format_duration_string(result):
    # Format duration string to HH:MM:SS format
    parts = result.split(':')
    formatted_parts = [part.zfill(2) for part in parts]
    if len(formatted_parts) < 3:
        formatted_parts = ['00'] * (3 - len(formatted_parts)) + formatted_parts
    formatted_duration = ':'.join(formatted_parts)
    return formatted_duration


def convert_to_mp3(mp4_path, mp3_path):
    # Convert given file
    file_to_convert = AudioFileClip(mp4_path)
    file_to_convert.write_audiofile(mp3_path)
    file_to_convert.close()
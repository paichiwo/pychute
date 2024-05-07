from moviepy.editor import AudioFileClip
from datetime import datetime


def format_date_string(result):
    # Format date string to DD-MM-YYYY HH:MM:SS format
    date_stripped = result[20:-10] + result[-8:-2]
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

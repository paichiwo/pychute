from datetime import datetime
import re


def format_date_string(date_str):
    # Clean up the date string by removing unnecessary text and whitespace
    date_stripped = date_str.strip().replace("First published at ", "").strip()

    # Remove any ordinal suffixes like 'st', 'nd', 'rd', 'th' using regex
    date_stripped = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_stripped)

    # Remove any trailing period
    date_stripped = date_stripped.rstrip('.')

    # Parse the cleaned date string
    try:
        date = datetime.strptime(date_stripped, '%H:%M %Z on %B %d, %Y')
        return date.strftime('%d-%m-%Y %H:%M:%S')
    except ValueError as e:
        # Handle the error if date format is still not matching
        raise ValueError(f"Could not parse date: '{date_stripped}' with error: {e}")


def format_duration_string(result):
    # Format duration string to HH:MM:SS format
    parts = result.split(':')
    formatted_parts = [part.zfill(2) for part in parts]
    if len(formatted_parts) < 3:
        formatted_parts = ['00'] * (3 - len(formatted_parts)) + formatted_parts
    formatted_duration = ':'.join(formatted_parts)
    return formatted_duration

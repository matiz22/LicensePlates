import re


def clean_license_plate_text(text):
    if not text:
        return ""

    text = text.upper()
    text = ''.join(text.split())

    valid_chars = re.compile(r'[A-Z0-9]')
    cleaned_text = ''.join(c for c in text if valid_chars.match(c))

    char_replacements = {
        'O': '0', 'I': '1', 'B': '8', 'S': '5', 'Z': '2', 'G': '6', 'D': '0',
    }

    return cleaned_text
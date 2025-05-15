def is_valid_plate_length(text, min_length=5, max_length=8):
    if not text:
        return False

    text_length = len(text)
    return min_length <= text_length <= max_length

def is_valid_plate_text(text):
    """
    Validate if the text resembles a license plate.

    Args:
        text: The text to validate

    Returns:
        Boolean indicating if the text is valid
    """
    return 5 <= len(text) <= 8

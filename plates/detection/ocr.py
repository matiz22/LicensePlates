import re

from easyocr import easyocr

reader = easyocr.Reader(["en"], gpu=True)


def perform_ocr(img, low_contrast=False):
    """
    Perform OCR on the provided image.

    Args:
        img: The image to perform OCR on
        low_contrast: Whether to use lower contrast threshold

    Returns:
        List of OCR detection results
    """
    try:
        params = {"allowlist": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"}

        if low_contrast:
            params["contrast_ths"] = 0.1

        return reader.readtext(img, **params)
    except Exception as e:
        print(f"OCR error: {e}")
        return []


def extract_best_plate_text(ocr_results):
    """
    Extract the best license plate text from OCR results.

    Args:
        ocr_results: List of OCR detection results

    Returns:
        Tuple of (best_text, best_confidence)
    """
    best_text = ""
    best_confidence = 0

    for detection in ocr_results:
        text = detection[1]
        confidence = detection[2]

        cleaned_text = re.sub(r"[^A-Z0-9]", "", text)

        if 5 <= len(cleaned_text) <= 8 and confidence > best_confidence:
            best_text = cleaned_text
            best_confidence = confidence

    return best_text, best_confidence

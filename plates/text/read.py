import easyocr

from plates.detection.ocr import perform_ocr, extract_best_plate_text
from plates.process.preprocess_ocr import preprocess_ocr
from plates.validate.plate import is_valid_plate_text


def read_plate_text(binary):
    """
    Extract text from a license plate image using EasyOCR with focus on license plate characters.

    Args:
        binary: Binary image of the license plate

    Returns:
        Tuple of (success, plate_text)
    """
    if binary is None:
        return False, ""

    processed_img = preprocess_ocr(binary)
    if processed_img is None:
        return False, ""

    ocr_results = perform_ocr(processed_img)
    best_text, _ = extract_best_plate_text(ocr_results)

    if not best_text:
        ocr_results = perform_ocr(processed_img, low_contrast=True)
        best_text, _ = extract_best_plate_text(ocr_results)

    if is_valid_plate_text(best_text):
        return True, best_text
    else:
        return False, ""

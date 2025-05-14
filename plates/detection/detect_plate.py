import os
import cv2

from plates.process.is_red_sticker import is_red_sticker
from plates.utils.image_utils import load_image
from plates.process.plate_dimensions import (
    has_valid_plate_dimensions,
    is_proper_rectangle,
)
from plates.process.preprocess_image import preprocess_image


def detect_plates_via_contours(image, edged):
    """Detect license plates using contour method.

    This function identifies potential license plates by analyzing contours in the processed image.
    It filters contours based on their shape and size to identify plate-like regions.
    - Considers only contours with 4-6 points, indicating rectangular or near-rectangular shapes.
    - Checks if the contour forms a valid plate-sized region based on its bounding dimensions.
    - Excludes regions that are identified as red stickers.
    - Prioritizes true rectangles if the contour has more than 4 points.

    Args:
        image (numpy.ndarray): The original color image.
        edged (numpy.ndarray): The edge-detected version of the image.

    Returns:
        list: A list of candidate plates as (x, y, width, height, area) tuples.
    """
    img_height, img_width = image.shape[:2]
    candidate_plates = []

    contours, _ = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if 4 <= len(approx) <= 6:
            x, y, w, h = cv2.boundingRect(approx)

            if has_valid_plate_dimensions(x, y, w, h, img_width, img_height):
                region = image[y : y + h, x : x + w]

                if not is_red_sticker(region):
                    if len(approx) != 4 or is_proper_rectangle(approx):
                        candidate_plates.append((x, y, w, h, cv2.contourArea(contour)))

    return candidate_plates


def detect_plates_via_cascade(image, processed_images):
    """Detect license plates using cascade classifier as fallback.

    Uses Haar cascade classifiers to detect potential license plates as a secondary method when
    contour-based detection fails. It attempts detection with multiple image processing techniques
    to maximize the chance of finding plates.
    - Uses different parameter sets to handle varying plate sizes and noise levels.
    - Filters out regions that do not meet basic plate dimensions or contain red stickers.
    - Returns the largest detected valid plate region if multiple candidates are found.

    Args:
        image (numpy.ndarray): The original color image.
        processed_images (dict): Dictionary containing various processed versions of the image.

    Returns:
        list: A list of detected valid plates as (x, y, width, height) tuples, or an empty list.
    """
    img_height, img_width = image.shape[:2]
    cascade_path = cv2.data.haarcascades + "haarcascade_russian_plate_number.xml"
    plate_cascade = cv2.CascadeClassifier(cascade_path)

    detection_attempts = [
        (processed_images["gray"], 1.1, 5, (30, 30)),
        (processed_images["blur"], 1.05, 4, (25, 25)),
        (processed_images["gray"], 1.03, 3, (20, 20)),
    ]

    for img, scale_factor, min_neighbors, min_size in detection_attempts:
        plates = plate_cascade.detectMultiScale(
            img, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size
        )

        valid_plates = []
        for x, y, w, h in plates:
            if has_valid_plate_dimensions(x, y, w, h, img_width, img_height):
                region = image[y : y + h, x : x + w]
                if not is_red_sticker(region):
                    valid_plates.append((x, y, w, h))

        if valid_plates:
            valid_plates.sort(key=lambda p: p[2], reverse=True)
            return valid_plates

    return []


def detect_license_plate(image_path, output_path="output"):
    """Detects and extracts license plates from an image and performs OCR to read the plate text.

    This function loads an image, preprocesses it, and attempts to locate license plates using
    both contour and cascade methods. If a plate is found, it extracts the region and prepares it for OCR.
    - Creates the output directory if it doesn't exist.
    - Returns the cropped plate image, its location, and a binary version for OCR.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Directory to save output files (if needed).

    Returns:
        tuple: (success, plate_img, plate_region, binary_plate)
            - success (bool): Whether a plate was detected.
            - plate_img (numpy.ndarray or None): The cropped license plate image.
            - plate_region (tuple or None): (x, y, width, height) of the plate region.
            - binary_plate (numpy.ndarray or None): Thresholded version of the plate for OCR.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image = load_image(image_path)
    if image is None:
        return False, None, None, None

    processed_images = preprocess_image(image)

    candidate_plates = detect_plates_via_contours(image, processed_images["edged"])

    if candidate_plates:
        candidate_plates.sort(key=lambda p: p[4], reverse=True)
        x, y, w, h, _ = candidate_plates[0]
        plate_img = image[y : y + h, x : x + w]
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        _, binary_plate = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return True, plate_img, (x, y, w, h), binary_plate

    valid_plates = detect_plates_via_cascade(image, processed_images)

    if valid_plates:
        x, y, w, h = valid_plates[0]
        plate_img = image[y : y + h, x : x + w]
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        _, binary_plate = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return True, plate_img, (x, y, w, h), binary_plate

    print("No license plates detected in the image")
    return False, None, None, None

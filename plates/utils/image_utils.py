import os
import cv2


def load_image(image_path):
    """Load an image from the given path."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image at {image_path}")
        return None
    return image


def enhance_and_save_plate(plate_img, output_path, image_path):
    """Enhance the detected plate and save both original and enhanced versions."""
    plate_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    _, plate_binary = cv2.threshold(
        plate_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    output_file = os.path.join(output_path, os.path.basename(image_path))
    cv2.imwrite(output_file, plate_img)

    enhanced_output = os.path.join(
        output_path, f"enhanced_{os.path.basename(image_path)}"
    )
    cv2.imwrite(enhanced_output, plate_binary)

    return output_file

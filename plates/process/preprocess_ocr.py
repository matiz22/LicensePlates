import cv2


def preprocess_ocr(binary_img):
    """Preprocess the binary image for better OCR performance.

    This function prepares the binary image for optimal text recognition by performing the following steps:
    - Resizing the image to improve OCR accuracy.
    - Converting the image to RGB format as required by OCR libraries like EasyOCR.

    Parameters:
    binary_img : np.ndarray
        The binary image to preprocess.

    Returns:
    np.ndarray or None
        The preprocessed image in RGB format or None if the input is invalid.
    """
    if binary_img is None:
        return None

    img = binary_img.copy()
    height, width = img.shape
    img = cv2.resize(img, (width * 3, height * 3))
    img_rgb = cv2.cvtColor(cv2.merge([img, img, img]), cv2.COLOR_BGR2RGB)

    return img_rgb

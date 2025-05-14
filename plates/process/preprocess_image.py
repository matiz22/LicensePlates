import cv2


def preprocess_image(image):
    """Apply preprocessing techniques to prepare image for license plate detection.

    This function performs several steps to enhance the image and extract the most relevant features for license plate detection, including:
    - Converting to grayscale.
    - Applying bilateral filtering for noise reduction.
    - Using adaptive thresholding to highlight key features.
    - Performing morphological closing to fill small gaps.
    - Detecting edges to isolate potential regions of interest.

    Parameters:
    image : np.ndarray
        The input color image (BGR format) to be preprocessed.

    Returns:
    dict
        A dictionary containing intermediate processing stages:
        - 'gray': Grayscale image.
        - 'blur': Denoised image after bilateral filtering.
        - 'edged': Edge-detected binary image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    edged = cv2.Canny(morph, 30, 200)

    return {"gray": gray, "blur": blur, "edged": edged}

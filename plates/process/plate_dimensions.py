import numpy as np


def has_valid_plate_dimensions(x, y, w, h, img_width, img_height):
    """Check if the region has valid dimensions for a license plate.

    Valid dimensions are determined based on the following criteria:
    - The aspect ratio (width / height) must be between 2.0 and 6.0.
    - The width must be at least 8% of the image width and at most 90%.
    - The height must be at least 2% of the image height and at most 30%.

    Parameters:
    x, y : int
        Top-left coordinates of the bounding box.
    w, h : int
        Width and height of the bounding box.
    img_width, img_height : int
        Dimensions of the full image.

    Returns:
    bool
        True if the dimensions match typical license plate proportions, False otherwise.
    """
    aspect_ratio = w / float(h)
    return (
        2.0 < aspect_ratio < 6.0
        and w > img_width * 0.08
        and h > img_height * 0.02
        and w < img_width * 0.9
        and h < img_height * 0.3
    )


def is_proper_rectangle(approx):
    """Check if the contour forms a proper rectangle (not just a parallelogram).

    This function checks if a given contour approximates a rectangle based on the following criteria:
    - The contour must have exactly 4 vertices.
    - All interior angles should be close to 90 degrees (within 15 degrees tolerance).

    Parameters:
    approx : list
        List of contour points, typically obtained from cv2.approxPolyDP().

    Returns:
    bool
        True if the contour is approximately rectangular, False otherwise.
    """
    if len(approx) != 4:
        return False

    angles = []
    for i in range(4):
        p1 = approx[i][0]
        p2 = approx[(i + 1) % 4][0]
        p3 = approx[(i + 2) % 4][0]

        v1 = p2 - p1
        v2 = p3 - p2

        dot = np.dot(v1, v2)
        det = v1[0] * v2[1] - v1[1] * v2[0]
        angle = abs(np.degrees(np.arctan2(det, dot)))
        angles.append(angle)

    angle_diffs = [abs(angle - 90) for angle in angles]
    return max(angle_diffs) < 15

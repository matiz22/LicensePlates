import cv2
import numpy as np


def is_red_sticker(region):
    """Check if the region is predominantly red (like barrier stickers).
    Solution for red stickers on barrier"""
    hsv_region = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_region, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_region, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    h, w = region.shape[:2]
    red_percentage = (np.sum(red_mask > 0) / (w * h)) * 100

    return red_percentage >= 40

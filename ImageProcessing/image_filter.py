"""Basic image filter to apply"""

import cv2

def bgr_color_filter(image, lower_color, upper_color):
    """Return the filtred image according to lower and upper color in BGR"""
    filtered_image = cv2.inRange(image, lower_color, upper_color)
    return filtered_image

def hsv_color_filter(image, lower_color, upper_color):
    """Return the filtred image according to lower and upper color in HSV"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    filtered_image = cv2.inRange(hsv,(10, 100, 20), (25, 255, 255))
    return filtered_image

    
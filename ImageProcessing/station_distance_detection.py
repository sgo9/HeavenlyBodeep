"""Define the function to compute the distance between the astronaut and the station"""

import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist

from utils import centeroidnp
from image_filter import bgr_color_filter

def astronaut_detection(image):
    """Return the approximate coordinates of the astronaut"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask_astro = cv2.inRange(hsv, (15, 100, 20), (25, 255, 255))
    white_pixels = cv2.findNonZero(mask_astro)
    white_pixels = np.reshape(white_pixels,(white_pixels.shape[0],2))

    astro_center = centeroidnp(white_pixels)
    return (int(astro_center[0]),int(astro_center[1]))


def station_distance(image):
    """Return the distance between astronaut and station, in pixels"""

    #filter blue colors to remove the planet in the background
    lower_blue = np.array([60, 35, 95])
    upper_blue = np.array([180, 255, 255])
    mask = bgr_color_filter(image, lower_blue, upper_blue)

    # perform a dilation + erosion to close gaps in between object edges
    edged = cv2.dilate(mask, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours individually
    mask = np.zeros_like(edged)
    list_xy = []
    astro_center = astronaut_detection(image)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 10:
            cv2.fillPoly(mask, [c], 255)
        rect = cv2.boundingRect(c)
        if rect[2] < 40 or rect[3] < 40: 
            continue
        
        x,y,w,h = rect
        list_xy.append((x+w/2,y+h/2))

    # find the bounding box with the astronaut
    austronaut_index = dist.cdist([astro_center],list_xy).argmin(axis=1)[0]
    austronaut_coord = list_xy[austronaut_index]
    list_xy.pop(austronaut_index)

    # measure distances between the astronaut and other objects, return the min
    s1 = np.array([austronaut_coord])
    s2 = np.array(list_xy)
    min_dist = dist.cdist(s1,np.array([centeroidnp(s2)])).min(axis=1)[0]

    return int(min_dist)
    

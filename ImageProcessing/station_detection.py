"""Define the function to compute the distance between the astronaut and the station"""

import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist
import os

from ImageProcessing.utils import centeroidnp
from ImageProcessing.image_filter import bgr_color_filter

def astronaut_detection(image):
    """Return the approximate coordinates of the astronaut"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask_astro = cv2.inRange(hsv, (15, 100, 20), (25, 255, 255))
    white_pixels = cv2.findNonZero(mask_astro)
    if white_pixels is None:
        return None
    white_pixels = np.reshape(white_pixels,(white_pixels.shape[0],2))

    astro_center = centeroidnp(white_pixels)
    return (int(astro_center[0]),int(astro_center[1]))


def station_polar_coordinates(image, screenshot_saved=False,image_name=1):
    """Return the distance and angle in radians between astronaut and station, in pixels"""
    image= cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
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

    if astro_center is None:
        return None, None

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
    if len(list_xy) < 2:
        return None,None
        
    astronaut_index = dist.cdist([astro_center],list_xy).argmin(axis=1)[0]
    astronaut_coord = list_xy[astronaut_index]
    list_xy.pop(astronaut_index)


    # measure distances between the astronaut and other objects, return the min
    astronaut_x, astronaut_y = astronaut_coord
    station_x, station_y = centeroidnp(np.array(list_xy))

    # compute distance
    astronaut_station_distance = int(((station_x-astronaut_x)**2+(station_y-astronaut_y)**2)**0.5)

    # compute angle
    if station_y-astronaut_y==0:
        astronaut_station_angle = np.pi/2
    else:
        astronaut_station_angle = round(np.arctan((station_x-astronaut_x)/(station_y-astronaut_y)),3)
    if station_x-astronaut_x > 0:
        astronaut_station_angle = np.pi + astronaut_station_angle

    if screenshot_saved:
        start_point = (int(astronaut_x),int(astronaut_y))
        end_point = (int(station_x),int(station_y))
        line = cv2.line(edged,start_point, end_point, (255,0,0), 2)   
        image_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'AstroBot','Screenshot',f'{image_name}.jpg')
        cv2.imwrite(image_path, line)

    return astronaut_station_distance, astronaut_station_angle
    
if __name__=="__main__":

    image = cv2.imread('raw_data/120.png', cv2.IMREAD_COLOR)
    cv2.imshow('image',image)
    print(station_polar_coordinates(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
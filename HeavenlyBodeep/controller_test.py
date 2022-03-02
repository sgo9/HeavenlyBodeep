import matplotlib.pyplot as plt
import numpy as np
import cv2
import pyautogui
from scipy.spatial import distance as dist
import imutils

def test_filter():
    image = cv2.imread("../raw_data/101.png") #cv2.IMREAD_GRAYSCALE)

    # Threshold of blue in HSV space
    lower_blue = np.array([0, 215, 240])
    upper_blue = np.array([255, 230, 255])

    # preparing the mask to overlay
    mask = cv2.inRange(image, lower_blue, upper_blue)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 80  # minimum number of pixels making up a line
    max_line_gap = 30  # maximum gap in pixels between connectable line segments
    line_image = np.copy(mask) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(mask, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    if lines.any():
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,255,0),2)

        # Draw the lines on the  image
        lines_edges = cv2.addWeighted(mask, 0.8, line_image, 1, 0)

        cv2.imshow('frame', lines_edges)
        cv2.waitKey(0) 

        angle = -np.arctan((np.average(lines[:,:,2])-np.average(lines[:,:,0]))/(np.average(lines[:,:,3])-np.average(lines[:,:,1])))*180/np.pi
        print(angle, (180+angle)%180)

    cv2.imshow('frame', mask)
    cv2.waitKey(0) 
    cv2.destroyAllWindows() 

def image_filter(image, lower_color, upper_color):
    """Return the filtred image according to lower and upper color"""
    mask = cv2.inRange(image, lower_color, upper_color)
    return mask

def line_detection(image):
    """Return lines on a filtred image"""
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 80  # minimum number of pixels making up a line
    max_line_gap = 30  # maximum gap in pixels between connectable line segments
    lines = cv2.HoughLinesP(image, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    return lines

def lines_to_angle(lines, previous_angle=0):
    """Return angle interpretation of a group of lines"""
    try:
        angle = -np.arctan((np.average(lines[:,:,2])-np.average(lines[:,:,0]))/(np.average(lines[:,:,3])-np.average(lines[:,:,1])))*180/np.pi
        return angle
    except:
        return previous_angle


def stream_astronaut_angle():

    # Threshold of blue in HSV space
    lower_color = np.array([0, 215, 240])
    upper_color = np.array([255, 230, 255])

    while(1):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        

        mask = image_filter(image, lower_color, upper_color)
        cv2.imshow('frame', cv2.resize(mask, (760, 540)))
        lines = line_detection(mask)
        angle = lines_to_angle(lines)
        print(angle, 180+angle)

        cv2.waitKey(0)
    
    cv2.destroyAllWindows()


def stream_station_distance():

    #filter blue colors to remove the planet in the background
    lower_blue = np.array([60, 35, 95])
    upper_blue = np.array([180, 255, 255])

    while(1):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        mask = cv2.inRange(image, lower_blue, upper_blue)

        # perform edge detection, then perform a dilation + erosion to
        # close gaps in between object edges
        #edged = cv2.Canny(image, 90, 100)
        edged = cv2.dilate(mask, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        # find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        #initialisation of lists of x and y of the center of the bounding boxes
        list_xy = []

        # loop over the contours individually
        mask = np.zeros_like(edged)

        for c in cnts:
            area = cv2.contourArea(c)
            if area > 10:
                cv2.fillPoly(mask, [c], 255)
            rect = cv2.boundingRect(c)
            if rect[2] < 40 or rect[3] < 40: 
                continue
            
            x,y,w,h = rect
            list_xy.append((x+w/2,y+h/2))
            cv2.rectangle(mask,(x,y),(x+w,y+h),(255,0,0),1)
            cv2.circle(mask,(int(mask.shape[1]/2),0),10,(255, 0, 0),1)

        austronaut_index = dist.cdist([(mask.shape[1]/2,mask.shape[0]/2)],list_xy).argmin(axis=1)[0]
        austronaut_coord = list_xy[austronaut_index]
        list_xy.pop(austronaut_index)

        s1 = np.array([austronaut_coord])
        s2 = np.array(list_xy)
        distance = dist.cdist(s1,s2).min(axis=1)


        print(distance)

    
    cv2.destroyAllWindows()

if __name__=="__main__":
    stream_station_distance()
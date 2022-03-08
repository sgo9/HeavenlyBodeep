import cv2
import numpy as np
from matplotlib import pyplot as plt
# from tensorflow.keras.backend import expand_dims
from ImageProcessing.station_detection import astronaut_detection
import imutils
import math
import pyautogui
import time

import os

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'raw_data', 'detection_chevron')
# print(path)
# image = cv2.imread(os.path.join(path, 'Screen_cap(8).png'))

def chevron_angle(image):
	'''Returns the angle between the chevron and the player when flying away from the station
	Angle from [0, 2*Pi]
	--------Input--------
	image : PIL screenshot (eg : pyautoguy.screenshot)
	--------Output-------
	angle : [0, 2*Pi]
	'''
	#changing from PIL image to np.array
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)

	#filtering on chevron
	low_white = np.array([0, 0, 250])
	up_white = np.array([255, 5, 255])
	mask = cv2.inRange(image, low_white, up_white).copy()
	mask_crop = mask.copy()
	mask_crop[:,:150] = 0
	mask_crop[:150,:] = 0
	mask_crop[930:,:] = 0
	mask_crop[:,1770:] = 0
	mask = mask - mask_crop

	#detecting contours of the shapes left in the edges of the mask
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	#looping over the contours
	list_xy = []
	for c in cnts:

		area = cv2.contourArea(c)
		if area > 10:
			cv2.fillPoly(mask, [c], 255)
		rect = cv2.boundingRect(c)

		#condition on bounding box with the usual shape of the chevron's bounding box
		if rect[2] not in range(44,57) and rect[3] not in range(44,57): 
			continue
		print(rect)
		x,y,w,h = rect
		list_xy.append((x+w/2,y+h/2))
		cv2.rectangle(mask,(x,y),(x+w,y+h),(255,0,0),1)

	if len(list_xy) == 0:
		return None
	#sin is the vertical axis
	sin = (1920/2 - list_xy[0][0])/((1920)/2)
	#cos is the horizontal axis
	cos = (1080/2 - list_xy[0][1])/((1080)/2)
	angle = math.atan2(sin, cos)
	angle = (angle + 2*np.pi) % (2*np.pi)
	return angle

if __name__ == '__main__':
	time.sleep(3)
	image = pyautogui.screenshot()
	cv2.imwrite(os.path.join(path,'screen.png'), np.array(image))
	print(chevron_angle(image))

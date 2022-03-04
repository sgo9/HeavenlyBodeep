import numpy as np
import cv2
import pyautogui
from ImageProcessing.station_detection import station_polar_coordinates


def stream_station_distance():

    while(1):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        polar_coords = station_polar_coordinates(image)
        print(polar_coords)

    
    cv2.destroyAllWindows()

if __name__=="__main__":
    stream_station_distance()
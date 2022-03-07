import numpy as np
import cv2
import pyautogui
from ImageProcessing.station_detection import station_polar_coordinates


def start():
    """Start deep controller"""
    print('\nWelcome to deep controller.\n')

    mode_details = """
    Select camera correction mode:
    1 - no camera correction
    2 - camera correction in game (X control)
    3 - camera correction with angle prediction model

    """

    mode_selection = 0
    while mode_selection not in [1,2,3]:
        mode_selection = int(input(mode_details))

    return mode_selection

def stream_station_distance():

    while(1):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        polar_coords = station_polar_coordinates(image)
        print(polar_coords)

    
    cv2.destroyAllWindows()

if __name__=="__main__":
    start()
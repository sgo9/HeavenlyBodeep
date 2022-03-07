from matplotlib import image
from ImageProcessing.station_detection import station_polar_coordinates
import pyautogui

#To be instanciated in reset function 
distances=[]


image=pyautogui.screenshot()
astronaut_station_distance, _=station_polar_coordinates(image)
distances.append(astronaut_station_distance)
if len(distances)==3:
    distances=distances[1:]



def reward(distances):
    ''' return reward based on 3 distances'''
    return 2*distances[1]-distances[0]-distances[2]
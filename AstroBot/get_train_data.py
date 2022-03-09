from distutils.util import check_environ
from json import tool
import numpy as np
import pandas as pd
import os
import pyvjoy
from datetime import datetime
import pyautogui
from time import sleep

from AstroBot.action_space import generate_movement_dict
from AstroBot.dummy_bot import dummy_decision
from HeavenlyBodeep.deep_controller import update_vjoy
from HeavenlyBodeep.predict_angle_correction import compute_angle_correction
from ImageProcessing.station_detection import station_polar_coordinates
from ImageProcessing.chevron_detection import chevron_angle

# Ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow.keras import models

# IgnoringStop ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' 



def execute_movement(j, move, angle_correction):
    for player_position in move:
        update_vjoy(j, player_position, {}, angle_correction)
        sleep(0.1)

def train_dummy_bot(move_number):

    # For VJoy output:
    j = pyvjoy.VJoyDevice(1)

    #importing model for angle correction:
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
    model = models.load_model(model_path)

    # importing movement dictionnary
    movement_dict = generate_movement_dict()

    log_dict = {'Id':[], 'Time': [], 'Move':[], 'Station_Distance': [], 'Station_Angle':[], 'Astronaut_Angle':[]}
    station_angle_memory, toggle_angle_memory = 0, np.pi

    for _ in range(move_number):

        # environment
        game_image = pyautogui.screenshot()
        
        # observation
        astronaut_angle = compute_angle_correction(game_image, model)
        #game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) # TODO remove this line -- integrated in ImageProcessing
        station_distance, station_angle = station_polar_coordinates(game_image)
        toggle_angle = chevron_angle(game_image)

        if (station_distance is None or station_angle is None) and toggle_angle is not None:
            image_name = f"ss_m{_}_sd{'xxx'}_sa{'xxx'}_aa{int(astronaut_angle*180/np.pi)}_ca{int(toggle_angle*180/np.pi)}"
        elif station_distance is not None and station_angle is not None and toggle_angle is None:
            image_name = f"ss_m{_}_sd{station_distance}_sa{int(station_angle*180/np.pi)}_aa{int(astronaut_angle*180/np.pi)}_ca{'xxx'}"
        elif station_distance is None and station_angle is None and toggle_angle is None:
            image_name = f"ss_m{_}_sd{'xxx'}_sa{'xxx'}_aa{int(astronaut_angle*180/np.pi)}_ca{'xxx'}"
        else:
            image_name = f"ss_m{_}_sd{station_distance}_sa{int(station_angle*180/np.pi)}_aa{int(astronaut_angle*180/np.pi)}_ca{int(toggle_angle*180/np.pi)}"
        station_polar_coordinates(game_image, screenshot_saved=True, image_name=image_name)

        # station angle memory
        if station_angle == None:
            station_angle = station_angle_memory
        station_angle_memory = station_angle

        # togle angle memory
        if toggle_angle == None:
            toggle_angle = toggle_angle_memory
        toggle_angle_memory = toggle_angle

        # action with dummy_bot
        move_key = dummy_decision(500, toggle_angle, astronaut_angle)

        move = movement_dict[move_key]
        execute_movement(j, move, astronaut_angle)

        # log
        log_dict['Id'].append(_)
        log_dict['Time'].append(datetime.now()) # TODO try DateTime.Now.ToShortTimeString()
        log_dict['Move'].append(move_key)

        log_dict['Station_Distance'].append(station_distance)
        log_dict['Station_Angle'].append(station_angle)
        log_dict['Astronaut_Angle'].append(astronaut_angle)
        sleep(1)
        print(move_key, station_distance, int(station_angle*180/np.pi), int(astronaut_angle*180/np.pi))
        print(toggle_angle)

    df = pd.DataFrame(log_dict)
    df.to_csv('log_train.csv', index=False)

if __name__=="__main__":
    train_dummy_bot(200)



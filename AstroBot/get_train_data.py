import os
import pandas as pd
import random
from AstroBot.action_space import generate_movement_dict
from HeavenlyBodeep.deep_controller import update_vjoy
from ImageProcessing.station_detection import station_polar_coordinates
from HeavenlyBodeep.predict_angle_correction import compute_angle_correction
import pyvjoy
from datetime import datetime
import pyautogui
import cv2
import numpy as np
from time import sleep

# Ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow.keras import models

# IgnoringStop ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' 

# For VJoy output:
j = pyvjoy.VJoyDevice(1)

#importing model for angle correction:
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
model = models.load_model(model_path)


movement_dict = generate_movement_dict(100)

def execute_movement(move, angle_correction):
    print("arm_movement")
    for player_position in move:
        update_vjoy(j, player_position, {}, angle_correction)

log_dict = {'Id':[], 'Time': [], 'Move':[], 'Station_Distance': [], 'Station_Angle':[], 'Astronaut_Angle':[]}

training_time = 1000

for _ in range(training_time):


    # environment
    game_image = pyautogui.screenshot()
    
    # angle correction
    angle_correction = compute_angle_correction(game_image, model)

    # action
    move_key = random.randint(0,2)
    move = movement_dict[move_key]
    execute_movement(move, angle_correction)

    # observations
    log_dict['Id'].append(_)
    log_dict['Time'].append(datetime.now()) # TODO try DateTime.Now.ToShortTimeString()
    log_dict['Move'].append(move_key)
    game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) # TODO remove this line -- integrated in ImageProcessing
    distance, angle = station_polar_coordinates(game_image)
    log_dict['Station_Distance'].append(distance)
    log_dict['Station_Angle'].append(angle)
    log_dict['Astronaut_Angle'].append(angle)
    sleep(1)
    print(datetime.now(), move_key, distance, angle)

print(log_dict)
df = pd.DataFrame(log_dict)
df.to_csv('log_train.csv', index=False)





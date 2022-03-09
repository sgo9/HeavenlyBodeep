"""Use astronaut angle detection trained model to predict the camera correction"""
import os
import cv2
import math
import numpy as np

# Ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from tensorflow.keras.backend import expand_dims
from tensorflow.keras import models

# IgnoringStop ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

#useful only for tests
import matplotlib.pyplot as plt
import pyautogui
import time
from datetime import datetime



def compute_angle_correction(game_image, model):
    """Return the astronaut angle in radiant [0,2*pi] considering an image of the game 
    -------Args---------
    game_image - Must be PIL format (native format of pyautogui screenshots)
    model - must be a Tensorflow keras model, inputed by (None, 100, 100, 3) shape images
    
    ------Output---------
    outputs the angle (rad) of the astronaut"""

    processed_image = game_image.crop((690,270,1190,770)).resize((100,100))
    cos_sin = model.predict(expand_dims(processed_image,0))
    angle = math.atan2(cos_sin[0,1], cos_sin[0,0])
    #Calculating angles's modulo
    mod_angle = (angle + 2 * math.pi) % (2 * math.pi) 
    return mod_angle



if __name__ == '__main__':
    '''To test the main, lanch and go in game : it will log all the angles of the body !!!'''

    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
    model = models.load_model(model_path)
    time.sleep(5)
    while 1:
        image = pyautogui.screenshot()
        print(f'The angle is {compute_angle_correction(image,model)}. Time is {datetime.now().minute}min and {datetime.now().second} sec')
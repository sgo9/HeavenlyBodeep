import pyautogui
import time
from PIL import Image
import cv2
import numpy as np
from tensorflow import keras
import os
import sys
# while True:
#     time.sleep(2.0)

path=os.path.join(os.path.dirname(__file__),'model','rotation_model')

model = keras.models.load_model(path)

def get_angle(model):
    ''' Takes a screenshot and returns angular position '''
    img = pyautogui.screenshot()
    img=img.crop((660,240,1260,840)).resize((64,64))
    img_pred=np.array([np.array(img)[:,:,0:3]])
    pred=np.argmax(model.predict(img_pred), axis=-1)[0]*5
    return pred

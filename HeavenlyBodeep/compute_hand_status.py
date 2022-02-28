from cmath import pi
from math import asin
import numpy as np
import mediapipe as mp
mp_holistic = mp.solutions.holistic

def distance(x1, x2, y1, y2):
    """Return distance between two points in 2D dimension"""
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def compute_hand_status(results, discard_not_found=True):

    # check if one point is found by the pose detection model
    if results.pose_landmarks == None: # TODO also check if .x or .y >
        return {}

    if results.right_hand_landmarks:
        x_rh = [results.right_hand_landmarks.landmark[i].x for i in [0,9,12]]
        y_rh = [results.right_hand_landmarks.landmark[i].y for i in [0,9,12]]
 
        print('right hand',
                f'({distance(x_rh[2],x_rh[0],y_rh[2],y_rh[0])/distance(x_rh[1],x_rh[0],y_rh[1],y_rh[0])}'
            )
    if results.left_hand_landmarks:
        x_lh = [results.left_hand_landmarks.landmark[i].x for i in [0,9,12]]
        y_lh = [results.left_hand_landmarks.landmark[i].y for i in [0,9,12]]

        print('left hand',
                f'({distance(x_lh[2],x_lh[0],y_lh[2],y_lh[0])/distance(x_lh[1],x_lh[0],y_lh[1],y_lh[0])}'
            )
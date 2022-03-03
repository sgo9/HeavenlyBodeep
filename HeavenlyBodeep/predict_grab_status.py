"""Predict hand grab status using holistic result"""

from utils import distance


def compute_grab_status(results, discard_not_found=True):
    """Returns a dictionary with the hand status (opened or closed).
       If the hands are not in the frame, returns None"""
    
    # check if one point is found by the pose detection model
    if results.pose_landmarks == None: # TODO also check if .x or .y >
        return {}

    grab_status = {}

    # grab right hand
    if results.right_hand_landmarks:
        # computations of the distances between the wrist (point 0) and the top of the palm (point 9)
        # and the wrist (point 0) and the top of the middle finger (point 12)
        x_rh = [results.right_hand_landmarks.landmark[i].x for i in [0,9,12]]
        y_rh = [results.right_hand_landmarks.landmark[i].y for i in [0,9,12]]
 
        ratio_rh = distance(x_rh[2],x_rh[0],y_rh[2],y_rh[0])/distance(x_rh[1],x_rh[0],y_rh[1],y_rh[0])

        if ratio_rh > 1.7:
            grab_status['right_hand'] = 2 # right hand opened
        elif 1.2 < ratio_rh < 1.7:
            grab_status['right_hand'] = 1 # gray area --> do not update right hand status
        elif ratio_rh < 1.2:
            grab_status['right_hand'] = 0 # right hand closed
    else: grab_status['right_hand'] = None

            
    # grab left hand
    if results.left_hand_landmarks:
        # computations of the distances between the wrist (point 0) and the top of the palm (point 9)
        # and the wrist (point 0) and the top of the middle finger (point 12)
        x_lh = [results.left_hand_landmarks.landmark[i].x for i in [0,9,12]]
        y_lh = [results.left_hand_landmarks.landmark[i].y for i in [0,9,12]]

        ratio_lh = distance(x_lh[2],x_lh[0],y_lh[2],y_lh[0])/distance(x_lh[1],x_lh[0],y_lh[1],y_lh[0])

        if ratio_lh > 1.7:
            grab_status['left_hand'] = 2 # left hand opened
        elif 1.2 < ratio_lh < 1.7:
            grab_status['left_hand'] = 1 # gray area --> do not update left hand status
        elif ratio_lh < 1.2:
            grab_status['left_hand'] = 0 # left hand closed
    else: grab_status['left_hand'] = None

    return grab_status

def compute_grab_status(results):
    """Returns a dictionary with the hand status (opened or closed).
       If the hands are not in the frame, returns None"""
    
    # check if one point is found by the pose detection model
    if results.pose_landmarks == None: # TODO also check if .x or .y >
        return {}

    grab_status = {}

    # grab right hand
    if results.right_hand_landmarks:
        # computations of the distances between the wrist (point 0) and the top of the palm (point 9)
        # and the wrist (point 0) and the top of the middle finger (point 12)
        x_rh = [results.right_hand_landmarks.landmark[i].x for i in [0,9,12]]
        y_rh = [results.right_hand_landmarks.landmark[i].y for i in [0,9,12]]
 
        ratio_rh = distance(x_rh[2],x_rh[0],y_rh[2],y_rh[0])/distance(x_rh[1],x_rh[0],y_rh[1],y_rh[0])

        if ratio_rh < 1.2:
            grab_status['right_hand'] = True # right hand closed

         
    # grab left hand
    if results.left_hand_landmarks:
        # computations of the distances between the wrist (point 0) and the top of the palm (point 9)
        # and the wrist (point 0) and the top of the middle finger (point 12)
        x_lh = [results.left_hand_landmarks.landmark[i].x for i in [0,9,12]]
        y_lh = [results.left_hand_landmarks.landmark[i].y for i in [0,9,12]]

        ratio_lh = distance(x_lh[2],x_lh[0],y_lh[2],y_lh[0])/distance(x_lh[1],x_lh[0],y_lh[1],y_lh[0])

        if ratio_lh < 1.2:
            grab_status['left_hand'] = True # left hand closed

    return grab_status
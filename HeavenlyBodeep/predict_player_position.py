
# results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
#from cmath import pi
from math import acos
import mediapipe as mp
mp_holistic = mp.solutions.holistic

def distance(x1, x2, y1, y2):
    """Return distance between two points in 2D dimension"""
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def compute_player_position(results, discard_not_found=True):

    # check if one point is found by the pose detection model
    if results.pose_landmarks == None:
        return {}

    # save the useful points (left and right shoulder, left and right wrist)
    pt_11 = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
    pt_12 = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
    pt_15 = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
    pt_16 = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
    pt_25 = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
    pt_26 = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]

    # check if all necessary points are found by the pose detection model
    if discard_not_found:
        min_pt = min([pt_11.x, pt_11.y, pt_12.x, pt_12.y, pt_15.x, pt_15.y, pt_16.x, pt_16.y])
        max_pt = max([pt_11.x, pt_11.y, pt_12.x, pt_12.y, pt_15.x, pt_15.y, pt_16.x, pt_16.y])
        if min_pt < 0 or max_pt > 1:
            return {}

    # compute normalization factor
    arm_body_ratio = 1.5 #TODO adapt to real measures
    body_size = distance(pt_11.x, pt_12.x, pt_11.y, pt_12.y) # distance between shoulders
    normalization_factor = body_size * arm_body_ratio

    # compute hand distances
    right_hand_dist = distance(pt_16.x, pt_12.x, pt_16.y, pt_12.y)/normalization_factor
    left_hand_dist = distance(pt_15.x, pt_11.x, pt_15.y, pt_11.y)/normalization_factor
    right_hand_dist_y = (pt_16.y-pt_12.y)/normalization_factor
    left_hand_dist_y = (pt_15.y-pt_11.y)/normalization_factor

    # compute hand angles
    left_hand_angle = (acos(left_hand_dist_y/left_hand_dist))
    right_hand_angle = (acos(right_hand_dist_y/right_hand_dist))

    # edit player position dictionnary
    player_position = {}
    player_position['left_hand_dist'] = left_hand_dist
    player_position['right_hand_dist'] = right_hand_dist
    player_position['left_hand_angle'] = left_hand_angle
    player_position['right_hand_angle'] = right_hand_angle

    # A command
    if (pt_15.x-pt_16.x)/normalization_factor <0.35:
        player_position['a_command'] = True
    else:
        player_position['a_command'] = False
        
    # legs status
    legs_position = min([abs(pt_25.y-pt_12.y)/normalization_factor, abs(pt_26.y-pt_11.y)/normalization_factor])
    if legs_position < 1.3:
        player_position['legs_status'] = True
    else:
        player_position['legs_status'] = False

    return player_position

if __name__=="__main__":
    pass
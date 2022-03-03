from math import acos, pi
import mediapipe as mp
from utils import distance

mp_holistic = mp.solutions.holistic

def compute_player_position(results, discard_not_found=True):

    # check if one point is found by the pose detection model
    if results.pose_landmarks == None:
        return {}

    # save the useful points (left and right shoulders, wrists and knees)
    pt_11 = results.pose_landmarks.landmark[11] # mp_holistic.PoseLandmark.LEFT_SHOULDER
    pt_12 = results.pose_landmarks.landmark[12] # mp_holistic.PoseLandmark.RIGHT_SHOULDER
    pt_15 = results.pose_landmarks.landmark[15] # mp_holistic.PoseLandmark.LEFT_WRIST
    pt_16 = results.pose_landmarks.landmark[16] # mp_holistic.PoseLandmark.RIGHT_WRIST
    pt_25 = results.pose_landmarks.landmark[25] # mp_holistic.PoseLandmark.LEFT_KNEE
    pt_26 = results.pose_landmarks.landmark[26] # mp_holistic.PoseLandmark.RIGHT_KNEE

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
    if pt_15.x-pt_11.x > 0:
        left_hand_angle = (acos(left_hand_dist_y/left_hand_dist))
    else:
        left_hand_angle = 2*pi-(acos(left_hand_dist_y/left_hand_dist))

    if pt_16.x-pt_12.x < 0:
        right_hand_angle = (acos(right_hand_dist_y/right_hand_dist))
    else:
        right_hand_angle = 2*pi-(acos(right_hand_dist_y/right_hand_dist))

    # edit player position dictionnary
    player_position = {}
    player_position['left_hand_dist'] = left_hand_dist
    player_position['right_hand_dist'] = right_hand_dist
    player_position['left_hand_angle'] = left_hand_angle
    player_position['right_hand_angle'] = right_hand_angle

    # A command
    player_position['a_command'] = (pt_15.x-pt_16.x)/normalization_factor < 0.35

    # legs status
    player_position['legs_status'] = min([abs(pt_25.y-pt_12.y), abs(pt_26.y-pt_11.y)])/normalization_factor < 1.3

    return player_position

if __name__=="__main__":
    pass
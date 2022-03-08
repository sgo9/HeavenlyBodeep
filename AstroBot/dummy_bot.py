"""Dummy bot functions : algo bot able to go back to the station when lost in deeper space"""

from random import randint
from numpy import cos, sin, pi

def angle_decision(station_angle, astronaut_angle, alignement_threshold):

    angle_delta = station_angle-astronaut_angle

    if cos(angle_delta) > alignement_threshold:
        return 2 # move forward with both arms

    if sin(angle_delta) > 0:
        return 0 # left turn

    return 1 # right turn 


def dummy_decision(station_distance, station_angle, astronaut_angle, station_too_close_distance=200, alignement_threshold=0.95):
    """Next dummy move to do to go back to the station:
    - if station is visible, align astronaut angle with station with left or right move, then advance with both arm move
    - if station is not visible, algin astronaut angle with toggle with left or right, then advance with both arm move
    - if station is too close, make a random move"""

    if station_distance is None: # station not visible
        return angle_decision(station_angle, astronaut_angle, alignement_threshold)

    elif station_distance > station_too_close_distance:
        return angle_decision(station_angle, astronaut_angle, alignement_threshold)

    return randint(0,2)

if __name__=='__main__':
    move_dict = {0:'left move',1:'right move',2:'both move'}

    print('station too close')
    # station too close
    move_index = dummy_decision(250, 0, 0, station_too_close_distance=300)
    print(move_dict[move_index])

    print('station aligned')
    # station aligned with astronaut
    move_index = dummy_decision(350, 0.3, 0.32, station_too_close_distance=300)
    print(move_dict[move_index])

    print('station on the left')
    # station on the left - without angle issue
    move_index = dummy_decision(350, 0.9, 0.1, station_too_close_distance=300)
    print(move_dict[move_index])

    # station on the left - with angle issue
    move_index = dummy_decision(350, 0.3, 6.2, station_too_close_distance=300)
    print(move_dict[move_index])

    print('station on the right')
    # station on the right - without angle issue
    move_index = dummy_decision(350, 3.14, 3.6, station_too_close_distance=300)
    print(move_dict[move_index])

    # station on the right - with angle issue
    move_index = dummy_decision(350, 6.1, 0.2, station_too_close_distance=300)
    print(move_dict[move_index])


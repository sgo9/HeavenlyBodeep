"""Define possible actions of the astronaut during bot training"""
from gevent import sleep
import pyvjoy
import numpy as np
from HeavenlyBodeep.deep_controller import update_vjoy
import time

# For VJoy output:
j = pyvjoy.VJoyDevice(1)

# simplified action space - 3 moves

def generate_movement_dict(slow=100):
    """Return a dictionnaire of basic swim moves, slow down movement frame to match with game"""
    
    movement_chain = [
        [0.2, 90],
        [1, 180],
        [1, 150],
        [1, 120],
        [1, 90],
        [1, 60],
        [1, 30],
        [1, 0],
        [0.5, 30],
        [0.3, 60]
    ]

    movement_chain_slowed = [movement_chain[i//slow] for i in range(slow*len(movement_chain))]
    left_arm_move, right_arm_move, both_arm_move = [], [], [] # list of players positions

    for mov_param in movement_chain_slowed:
        # left hand move
        player_position = {}
        player_position['left_hand_dist'] = mov_param[0]
        player_position['left_hand_angle'] = mov_param[1] * np.pi / 180
        player_position['right_hand_dist'] = movement_chain_slowed[0][0]
        player_position['right_hand_angle'] = movement_chain_slowed[0][1] * np.pi / 180
        left_arm_move.append(player_position)

        # right hand move
        player_position = {}
        player_position['left_hand_dist'] = movement_chain_slowed[0][0]
        player_position['left_hand_angle'] = movement_chain_slowed[0][1] * np.pi / 180
        player_position['right_hand_dist'] = mov_param[0]
        player_position['right_hand_angle'] =  mov_param[1] * np.pi / 180
        right_arm_move.append(player_position)

        # both arms move
        player_position = {}
        player_position['left_hand_dist'] = mov_param[0]
        player_position['left_hand_angle'] = mov_param[1] * np.pi / 180
        player_position['right_hand_dist'] = mov_param[0]
        player_position['right_hand_angle'] =  mov_param[1] * np.pi / 180
        both_arm_move.append(player_position)

    return {0:left_arm_move, 1: right_arm_move, 2: both_arm_move}

# continuous action space
#--> 4 axis, 4 continuous

# discrete action space
arm_angle_range = np.linspace(0,np.pi,4) # 4 possible angle on radians
arm_distance_range = np.linspace(0.2,1,2) #4 possible distance from 0.25 to full extention

arm_angle_matrix = np.array([[[left_angle, right_angle] for left_angle in arm_angle_range] for right_angle in arm_angle_range])


if __name__=="__main__":
    move = generate_movement_dict(slow=10)[1]
    print(move[1])
    for player_position in move:
        update_vjoy(j,player_position,{}, 0)

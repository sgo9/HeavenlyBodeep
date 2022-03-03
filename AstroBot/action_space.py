"""Define possible actions of the astronaut during bot training"""

import numpy as np
from HeavenlyBodeep.deep_controller import update_vjoy

# simplified action space - 2 moves
left_arm_move = list() # list of player position dictionnaries corresponding to left arm move

movement_params = [
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

    # player_position['left_hand_dist'] = left_hand_dist
    # player_position['right_hand_dist'] = right_hand_dist
    # player_position['left_hand_angle'] = left_hand_angle
    # player_position['right_hand_angle'] = right_hand_angle

left_arm_move = [{'left_hand_dist':mov_param[0], 'left_hand_dist':mov_param[0]} for mov_param in movement_params]

[[0.2,90]]
# continuous action space
#--> 4 axis, 4 continuous

# discrete action space
arm_angle_range = np.linspace(0,np.pi,4) # 4 possible angle on radians
arm_distance_range = np.linspace(0.2,1,2) #4 possible distance from 0.25 to full extention



arm_angle_matrix = np.array([[[left_angle, right_angle] for left_angle in arm_angle_range] for right_angle in arm_angle_range])
print('arm_angle_range',arm_angle_range)
print('arm_distance_range',arm_distance_range)
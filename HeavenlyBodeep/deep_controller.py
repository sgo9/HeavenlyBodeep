#  vJoy, pyVJoy and x360ce
# https://gamepad-tester.com/

from random import getrandbits
from math import cos, sin
import pyvjoy


def coordinate_correction(x):
    """Return joystick coordinate between 0x0000 (0) and 0x8000 (32768)"""
    if x > int(0x8000):
        return 0x8000
    elif x < int(0x0000):
        return 0x0000
    return int(x)


def compute_buttons_value(a_command, grab_left, grab_right, legs_status, reset_camera):
    """Return the decimal value corresponding to the binary mapping of buttons status
    a_command : b1 (2**0), grab_left : b5 (2**4), grab_right : b6 (2**5), legs : b7 + b8 (2**6+2**7)"""
    return a_command * 1 + grab_left * 16 +  grab_right * 32 + legs_status * 192 + reset_camera * getrandbits(1) * 4 


def update_vjoy(j, player_position, grab_status, angle_correction, camera_auto_rotation=False):
    """Main function of deep_controller
    Update joystick status according to player position and grab status"""

    if player_position:

        # joystick position (hands distance and position)

        left_hand_coordinate_x = int(0x4000)-(player_position['left_hand_dist'] * sin(player_position['left_hand_angle']-angle_correction))*int(0x4000)
        left_hand_coordinate_y = (player_position['left_hand_dist'] * -cos(player_position['left_hand_angle']-angle_correction))*int(0x4000)+int(0x4000)
        j.data.wAxisX = coordinate_correction(left_hand_coordinate_x)
        j.data.wAxisY = coordinate_correction(left_hand_coordinate_y)

        right_hand_coordinate_x = int(0x4000)+(player_position['right_hand_dist'] * sin(player_position['right_hand_angle']+angle_correction))*int(0x4000)
        right_hand_coordinate_y = (player_position['right_hand_dist'] * -cos(player_position['right_hand_angle']+angle_correction))*int(0x4000)+int(0x4000)
        j.data.wAxisYRot = coordinate_correction(right_hand_coordinate_x)
        j.data.wAxisXRot = coordinate_correction(right_hand_coordinate_y)


        # buttons status (A, left and right grab, legs status)

        a_command = player_position.get('a_command', False)
        grab_left = grab_status.get('left_hand', False)
        grab_right = grab_status.get('right_hand', False)
        legs_status = player_position.get('legs_status', False)
        reset_camera = player_position.get('x_command', False) or camera_auto_rotation

        j.data.lButtons = compute_buttons_value(a_command, grab_left, grab_right, legs_status, reset_camera)


    j.update() # update method to push joystick attributes at the same time and avoid saturation


if __name__=="__main__":

    j = pyvjoy.VJoyDevice(1)

    j.data.lButtons = 17
    j.update()

    a_command = True
    grab_left = False
    grab_right = True
    legs = True
    camera_auto_rotation = True
    j.data.lButtons = compute_buttons_value(a_command, grab_left, grab_right, legs, camera_auto_rotation)
    j.update()

    j.data.lButtons = 0
    j.update()
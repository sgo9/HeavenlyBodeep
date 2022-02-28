#  vJoy, pyVJoy and x360ce
# https://gamepad-tester.com/

import pyvjoy
import time
from cmath import pi
from math import cos, sin
sleep_time = 1
button_value = 1




def coordinate_correction(x):
    """Return joystick coordinate between 0 and 8000, int"""
    if x > int(0x8000):
        return 0x8000
    elif x < int(0x0000):
        return 0x0000
    return int(x)


def update_joystick(player_position, grab_status={'left':False, 'right':False}):
    # player_position['left_hand_dist']
    # player_position['right_hand_dist']
    # player_position['left_hand_angle']
    # player_position['right_hand_angle']

    #Pythonic API, item-at-a-time
    j = pyvjoy.VJoyDevice(1)

    if player_position:
        left_hand_coordinate_x = int(0x4000)-(player_position['left_hand_dist'] * sin(player_position['left_hand_angle']*pi/180))*int(0x4000)
        left_hand_coordinate_y = (player_position['left_hand_dist'] * -cos(player_position['left_hand_angle']*pi/180))*int(0x4000)+int(0x4000)
        j.data.wAxisX = coordinate_correction(left_hand_coordinate_x)
        j.data.wAxisY = coordinate_correction(left_hand_coordinate_y)

        right_hand_coordinate_x = int(0x4000)+(player_position['right_hand_dist'] * sin(player_position['right_hand_angle']*pi/180))*int(0x4000)
        right_hand_coordinate_y = (player_position['right_hand_dist'] * -cos(player_position['right_hand_angle']*pi/180))*int(0x4000)+int(0x4000)
        j.data.wAxisYRot = coordinate_correction(right_hand_coordinate_x)
        j.data.wAxisXRot = coordinate_correction(right_hand_coordinate_y)

    j.update()


if __name__=="__main__":

    #Pythonic API, item-at-a-time
    j = pyvjoy.VJoyDevice(1)
    time.sleep(sleep_time) # Sleep for 1 second
    # j.set_button(6,button_value)
    # time.sleep(sleep_time) # Sleep for 1 second
    # j.set_button(6,0)
    # j.set_button(5,button_value)
    # time.sleep(sleep_time) # Sleep for 1 second
    # j.set_button(5,0)

    print('next move')
    #j.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)
    #j.data.wAxisX = 0x8000 
    #j.data.wAxisY= 0x8000
    j.data.wAxisXRot = 0x8000
    j.data.wAxisYRot = 0x8000
    j.update()
    time.sleep(3) # Sleep for 1 second
    print('next move')

    j.data.wAxisX = 0x4000 
    j.data.wAxisY= 0x4000
    j.data.wAxisXRot = 0x4000
    j.data.wAxisYRot = 0x4000

    #send data to vJoy device
    j.update()
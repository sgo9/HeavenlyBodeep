#  vJoy, pyVJoy and x360ce
# https://gamepad-tester.com/

import pyvjoy
import time
from math import cos, sin

def coordinate_correction(x):
    """Return joystick coordinate between 0x0000 (0) and 0x8000 (32768)"""
    if x > int(0x8000):
        return 0x8000
    elif x < int(0x0000):
        return 0x0000
    return int(x)


def update_joystick(j, player_position):
    """Update joystick command according to player position"""
    # player_position['left_hand_dist','right_hand_dist','left_hand_angle','right_hand_angle']
    # grab_status['left', 'right'] --> 0 for release, 1 for neutral, 2 for grab

    if player_position:
        left_hand_coordinate_x = int(0x4000)-(player_position['left_hand_dist'] * sin(player_position['left_hand_angle']))*int(0x4000)
        left_hand_coordinate_y = (player_position['left_hand_dist'] * -cos(player_position['left_hand_angle']))*int(0x4000)+int(0x4000)
        j.data.wAxisX = coordinate_correction(left_hand_coordinate_x)
        j.data.wAxisY = coordinate_correction(left_hand_coordinate_y)

        right_hand_coordinate_x = int(0x4000)+(player_position['right_hand_dist'] * sin(player_position['right_hand_angle']))*int(0x4000)
        right_hand_coordinate_y = (player_position['right_hand_dist'] * -cos(player_position['right_hand_angle']))*int(0x4000)+int(0x4000)
        j.data.wAxisYRot = coordinate_correction(right_hand_coordinate_x)
        j.data.wAxisXRot = coordinate_correction(right_hand_coordinate_y)

    j.update()


def update_buttons(j, grab_status):
    """Update joystick command according to hand grab status"""
    if grab_status:
        if grab_status['left_hand'] == 0:
            j.set_button(5,1)
        elif grab_status['left_hand'] == 2:
            j.set_button(5,0)
        
        if grab_status['right_hand'] == 0:
            j.set_button(6,1)
        elif grab_status['right_hand'] == 2:
            j.set_button(6,0)



if __name__=="__main__":

    #Pythonic API, item-at-a-time
    j = pyvjoy.VJoyDevice(1)
    time.sleep(1) # Sleep for 1 second
    j.set_button(6,1)
    time.sleep(1) # Sleep for 1 second
    j.set_button(6,0)
    time.sleep(1) # Sleep for 1 second
    j.set_button(5,1)
    time.sleep(1) # Sleep for 1 second
    j.set_button(5,0)

    #send data to vJoy device
    j.update()
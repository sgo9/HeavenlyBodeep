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

class DeepController():

    def __init__(self):
        self.j=pyvjoy.VJoyDevice(1)
        self.left_hand_coordinate_x=int(0x4000)
        self.left_hand_coordinate_y=int(0x4000)
        self.right_hand_coordinate_x=int(0x4000)
        self.right_hand_coordinate_y=int(0x4000)
        self.threshold_movement=3000
        self.i=0

    def compute_buttons_value(self,a_command, grab_left, grab_right, legs_status, reset_camera):
        """Return the decimal value corresponding to the binary mapping of buttons status
        a_command : b1 (2**0), grab_left : b5 (2**4), grab_right : b6 (2**5), legs : b7 + b8 (2**6+2**7)"""
        return a_command * 1 + grab_left * 16 +  grab_right * 32 + legs_status * 192 + reset_camera * getrandbits(1) * 4 


    def update_vjoy(self, player_position, grab_status, angle_correction, camera_auto_rotation=False):
        """Main function of deep_controller
        Update joystick status according to player position and grab status"""

        if player_position:

            # joystick position (hands distance and position)
            new_left_hand_coordinate_x =coordinate_correction(int(0x4000)-(player_position['left_hand_dist'] * sin(player_position['left_hand_angle']-angle_correction))*int(0x4000))
            new_left_hand_coordinate_y =coordinate_correction((player_position['left_hand_dist'] * -cos(player_position['left_hand_angle']-angle_correction))*int(0x4000)+int(0x4000))
            
            if abs(new_left_hand_coordinate_x-self.left_hand_coordinate_x)<self.threshold_movement:
                #self.left_hand_coordinate_x=int(0x4000)
                self.j.data.wAxisX = int(0x4000)
            else:
                self.left_hand_coordinate_x=new_left_hand_coordinate_x
                self.j.data.wAxisX = self.left_hand_coordinate_x
            
            if abs(new_left_hand_coordinate_y-self.left_hand_coordinate_y)<self.threshold_movement:
                #self.left_hand_coordinate_y=int(0x4000)
                self.j.data.wAxisY = int(0x4000)
            else:
                self.left_hand_coordinate_y=new_left_hand_coordinate_y
                self.j.data.wAxisY = self.left_hand_coordinate_y

            new_right_hand_coordinate_y=coordinate_correction(int(0x4000)+(player_position['right_hand_dist'] * sin(player_position['right_hand_angle']+angle_correction))*int(0x4000))
            new_right_hand_coordinate_x =coordinate_correction((player_position['right_hand_dist'] * -cos(player_position['right_hand_angle']+angle_correction))*int(0x4000)+int(0x4000))

            if abs(new_right_hand_coordinate_x-self.right_hand_coordinate_x)<self.threshold_movement:
                #self.right_hand_coordinate_x=int(0x4000)
                self.j.data.wAxisXRot = int(0x4000)
            else:
                self.right_hand_coordinate_x=new_right_hand_coordinate_x
                self.j.data.wAxisXRot = self.right_hand_coordinate_x 
            
            if abs(new_right_hand_coordinate_y-self.right_hand_coordinate_y)<self.threshold_movement:
                #self.right_hand_coordinate_y=int(0x4000)
                self.j.data.wAxisYRot = int(0x4000)  
            else:
                self.right_hand_coordinate_y=new_right_hand_coordinate_y
                self.j.data.wAxisYRot = self.right_hand_coordinate_y
                        
            
            
            # buttons status (A, left and right grab, legs status)
            a_command = player_position.get('a_command', False)
            grab_left = grab_status.get('left_hand', False)
            grab_right = grab_status.get('right_hand', False)
            legs_status = player_position.get('legs_status', False)
            reset_camera = player_position.get('x_command', False) or camera_auto_rotation

            self.j.data.lButtons = self.compute_buttons_value(a_command, grab_left, grab_right, legs_status, reset_camera)
            self.j.update() # update method to push joystick attributes at the same time and avoid saturation


if __name__=="__main__":
    gamepad=DeepController()
    gamepad.j.update()
    print(gamepad.left_hand_coordinate_x)
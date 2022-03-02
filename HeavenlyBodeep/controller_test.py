import pyvjoy

j = pyvjoy.VJoyDevice(1)

j.data.lButtons = 678
j.update()
print('update finished')

def compute_buttons_value(a_command, grab_left, grab_right, legs):
    """Return the decimal value corresponding to the binary mapping of buttons status
    a_command : b1 (2**0), grab_left : b5 (2**4), grab_right : b6 (2**5), legs : b7 + b8 (2**6+2**7)"""
    return a_command * 1 + grab_left * 16 +  grab_right * 32 + legs * 192

a_command = True
grab_left = False
grab_right = True
legs = True
j.data.lButtons = compute_buttons_value(a_command, grab_left, grab_right, legs)
j.update()
import pyvjoy

j = pyvjoy.VJoyDevice(1)

j.buttons[1] = 1
j.update()
print('update finished')
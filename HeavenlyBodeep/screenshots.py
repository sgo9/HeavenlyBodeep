import pyautogui
from pynput.keyboard import Key, Controller
import os
import time
from datetime import datetime,timedelta
import pyvjoy
from inputs import get_gamepad



path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data')

def make_screenshot(file_name):
    pyautogui.screenshot(os.path.join(path,f'{file_name}.png'))


i=max([0]+[int(i[:-4]) for i in os.listdir(path) if i[-4:]==".png"])+1
time.sleep(5)
while True:
    make_screenshot(i)
    time.sleep(0.5)
    i += 1





i=max([int(i[:-4]) for i in os.listdir(path) if i[-4:]==".png"])+1
print(i)
# while True:
#     if i==0:
#         time.sleep(10)
#         i+=1
#     else:
#         time.sleep(1)
#         make_screenshot(i)
#         i+=1
#new_now=now+timedelta(seconds=5)
# now = datetime.now().second
# while True:
    
#     print(now-datetime.now().second)
    
    

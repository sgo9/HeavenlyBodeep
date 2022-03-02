import pyautogui
from pynput.keyboard import Key, Controller
import os
import time
from datetime import datetime,timedelta


path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data')

def make_screenshot(file_name):
    pyautogui.screenshot(os.path.join(path,f'{file_name}.png'))



# i=0
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
    
    

import pyautogui
from pynput.keyboard import Key, Controller
import os
import time


path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data')

def make_screenshot(file_name):
    keyboard = Controller()
    key = "c"
    time.sleep(0.3)
    keyboard.press(key)
    keyboard.release(key)
    pyautogui.screenshot(os.path.join(path,f'{file_name}.png'))



i=0
while True:
    if i==0:
        time.sleep(10)
        i+=1
    else:
        time.sleep(1)
        make_screenshot(i)
        i+=1





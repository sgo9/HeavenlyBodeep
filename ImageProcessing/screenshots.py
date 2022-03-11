import pyautogui
import os
import time


path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'raw_data')
print(path)

def make_screenshot(file_name):
    pyautogui.screenshot(os.path.join(path,f'{file_name}.png'))

if __name__ == "__main__":
    i=max([0]+[int(i[:-4]) for i in os.listdir(path) if i[-4:]==".png"])+1
    print(i)
    time.sleep(5)
    while True:
        make_screenshot(i)
        time.sleep(0.5)
        i += 1

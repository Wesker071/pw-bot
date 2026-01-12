import pyautogui
import cv2
import numpy as np

def looting_max_val(path):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)#вот

    screen_object = cv2.imread(path)
    screen_object = np.array(screen_object)
    screen_object = cv2.cvtColor(screen_object, cv2.COLOR_RGB2BGR)#вот

    result = cv2.matchTemplate(screenshot, screen_object, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    object_width = screen_object.shape[1]
    object_height = screen_object.shape[0]

    center_x = max_loc[0] + object_width // 2
    center_y = max_loc[1] + object_height // 2

    return min_val, max_val, min_loc, max_loc, center_x, center_y

def looting(paths):
    max_path = ''
    max_min_val = 0
    max_max_val = 0
    max_min_loc = 0
    max_max_loc = 0
    max_center_x = 0
    max_center_y = 0

    for path in paths:
        min_val, max_val, min_loc, max_loc, center_x, center_y = looting_max_val(path)
        if(max_val>max_max_val):
            max_path = path
            max_min_val = min_val
            max_max_val = max_val
            max_min_loc = min_loc
            max_max_loc = max_loc
            max_center_x = center_x
            max_center_y = center_y
    
    if(max_val>0.2):
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        print('max_val = ',max_val)
    else:
        print('Достойных совпадений нет', max_val)



    









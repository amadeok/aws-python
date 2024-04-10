import pyautogui
import sys

result = pyautogui.confirm(f'File could not be found: {sys.argv[1]}', buttons=['OK'])

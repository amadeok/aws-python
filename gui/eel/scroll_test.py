import pyautogui, win32api
from time import sleep

t = (901, 1350)
s = (1115, 1350)
n = 0
n2 = 0
scr = 50
sl = 0.5
scroll = 0
while 1:

    sleep(sl)
    if n % 2 == 0:
        pyautogui.click(t)
    else:
        pyautogui.click(s)
    sleep(sl)
    if scroll:
        for x in range(10):
            pyautogui.scroll( scr if n2 % 2 else -scr)
    n+=1
    if n %2 == 0: n2+=1
    
    if win32api.GetAsyncKeyState(27) == -32767:
        break

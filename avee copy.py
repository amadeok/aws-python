import win32gui,pywintypes
import win32con,win32file,win32pipe,win32api, numpy, threading
import pygetwindow as gw
import time, subprocess as sp, mss
from PIL import Image
import logging
# time.sleep(1)

import win32gui
import win32ui
import random
import autopy as at
from autopy import background_screenshot, receive_screen_shot_from_phone
import urllib.parse

import time
import pywinauto, ctypes, os
from urllib.parse import quote
from collections import namedtuple





os.system("taskkill /IM BleuPlayer.UWP.exe /F")
a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"
time.sleep(0.5)

proc = sp.Popen([a])
time.sleep(0.5)
win = gw.getWindowsWithTitle("Avee Player")[0]

#ret = background_screenshot(win._hWnd,win.width, win.height)
wid = win.width 
hei = win.height

r = (win.topleft.x, win.topleft.y, wid, hei)

template_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\AveeTemplate_normal\\"
audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"

nt = namedtuple("name_storage", "android_name win_name")

template_list = [nt(quote(elem), elem) for elem in os.listdir(template_fld)]
audio_list = [nt(quote(elem), elem) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

a = at.autopy("images_avee_win", img_prefix="") #w._hWnd
target_file =  random.choice(audio_list)
#target_file = nt(quote("s.mp3"), "s.mp3")# random.choice(audio_list)
file = audio_fld + "\\" + target_file.win_name #file = "file:///mnt/shared/Pictures/" + random.choice(audio_list).android_name #00024.wav"
file_cmd = f'start {file}'

temp_file = template_fld + "\\" + random.choice(template_list).win_name # CX%20liquify.viz"
temp_cmd = f'start  "{temp_file}"'

sleep_t = 2

import os
import subprocess

def start(filename):
    '''Open document with default application in Python.'''
    try:
        os.startfile(filename)
    except AttributeError:
        subprocess.call(['open', filename])


vis_found = a.find([a.i.visualizer], loop=3, region=r, grayscale=True, click=True)
if vis_found:
    a.click(vis_found.found, 0, 0)


time.sleep(sleep_t)

start(file)
time.sleep(sleep_t)

start(temp_file)
time.sleep(sleep_t)
#time.sleep(2)
a.click(vis_found.found, 120, 0) #clicking export
#wait for encode to finish and click the ad cross button
found = a.find([a.i.export2], loop=3, region=r, grayscale=True, click=True)

found = a.find([a.i.salva], loop=3, region=r, grayscale=True, click=True)

found = a.find([a.i.blue_cross], loop=3, region=r, grayscale=True)
t0 = time.time()
found = a.find([a.i.export2], loop=5, timeout=5*60, region=r, grayscale=True)
print("encode took ", time.time() - t0)
if found: #and  found == a.i.export:
    x = found.found[0] #- w.topleft.x
    y = found.found[1] #- w.topleft.y
    adb(f'input tap {x} {y}')



#ret = a.find(a.i.dict[prefix + "export_to_video_file"], loop=3, region=r, grayscale=True)

os.system(f"adb  -s emulator-5554 shell input keyevent 4") #back

#os.system(f'adb  -s emulator-5554 shell  am broadcast -a com.llamalab.automate.intent.action.START_FLOW -d content://com.llamalab.automate.provider/flows/8/statements/1 -n com.llamalab.automate/.StartServiceReceiver -e Payload "x{x_perc}x{y_perc}"')




# print(len(tot_data))
# with open("f.png", "wb") as f_o:
#     f_o.write(arr[0:pos])

# def send_page_down(handle, param):
#     if win32gui.GetClassName(handle) == param or 1:
#         win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
#         win32gui.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_UP, 0)

# G = gw.getWindowsWithTitle("Avee Player")
# G[0].moveTo(0, 0)
# window_id = win32gui.FindWindow(None, "Avee Player")
# win32gui.EnumChildWindows(window_id, send_page_down, 'FoxitDocWnd')
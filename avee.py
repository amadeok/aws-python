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






a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"

hwnd = win32gui.FindWindow(None, "LDPlayer")



def adb_output(cmd):
    process = sp.Popen(base + cmd,
                        shell=True,
                           stdout=sp.PIPE, 
                           stderr=sp.PIPE)

    out, err = process.communicate()
    errcode = process.returncode
    return out

def is_avee_running():
    ret =  adb_output(f"pidof com.daaw.avee")
    if ret != b'':
        return True
    return False
    
def check_avee_running():
    
    if not is_avee_running():
        logging.debug("Avee not running, starting")
        os.system(f"{base} am start -a android.intent.action.VIEW -n com.daaw.avee/.MainActivity")
        ret = a.find(a.i.speaker, loop=3, region=r)
        time.sleep(4)
    else:
        logging.debug("Avee running")


def adb(cmd):
    os.system(base + cmd)

def is_device_awake():
    ret = adb_output('dumpsys power | find "mWakefulness="')
    if "Awake" in str(ret): return True
    return False

def check_device_awake():
    if not is_device_awake():
        adb("input keyevent 26") #power
        logging.debug("powering up device")

wid = 1080 
hei = 2220

device = "ce041714f506223101" # emulator-5554
base = f"adb  -s {device} shell "

#background_screenshot(hwnd, wid, hei+52,True)
ret = receive_screen_shot_from_phone(save_file=True)

check_device_awake()

r = (0, 0, wid, hei)

prefix = "s8_"
template_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\AveeTemplate_normal\\"
audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"

nt = namedtuple("name_storage", "android_name win_name")

template_list = [nt(quote(elem), elem) for elem in os.listdir(template_fld)]
audio_list = [nt(quote(elem), elem) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

a = at.autopy("images_avee", ext_src="phone", img_prefix=prefix) #w._hWnd
a.ext_src_buffer =  bytearray(wid*hei*3)
target_file =  random.choice(audio_list)
#target_file = nt(quote("s.mp3"), "s.mp3")# random.choice(audio_list)
file = "file:///mnt/sdcard/input/audio/" + target_file.android_name #file = "file:///mnt/shared/Pictures/" + random.choice(audio_list).android_name #00024.wav"
file_cmd = f'{base} am start -a android.intent.action.VIEW -d "{file}" -n com.daaw.avee/.MainActivity'

temp_file = "file:///mnt/sdcard/input/templates/AveeTemplate_normal/" + random.choice(template_list).android_name # CX%20liquify.viz"
temp_cmd = f'{base} am start -a android.intent.action.VIEW -d "{temp_file}" -n com.daaw.avee/.MainActivity'

sleep_t = 2
os.system("adb start-server ")
os.system("adb start-server ")
adb("mkdir /mnt/sdcard/input ")
adb("mkdir /mnt/sdcard/input/audio ")
adb("mkdir /mnt/sdcard/input/templates")

adb("mkdir /mnt/sdcard/output ")
cmd = f'adb push ' + audio_fld.replace("\\", "/") +  target_file.win_name  + ' /mnt/sdcard/input/audio'
os.system(cmd)
#adb("cp " + audio_fld.replace("\\", "/") + file2.win_name +  " /mnt/sdcard/input" )
check_avee_running()

found = a.find(a.i.ad_cross, region=r, grayscale=True)
if found:
    x = found.found[0]# - w.topleft.x
    y = found.found[1]# - w.topleft.y
    adb(f'input tap {x} {y}')

time.sleep(sleep_t)

check_avee_running()
os.system(file_cmd)
time.sleep(sleep_t)

check_avee_running()
os.system(temp_cmd)
time.sleep(sleep_t)


def tab_scroll():
    logging.debug(f"Tab scrolling ")
    found = None
    for x in range(20):
        adb(f" input keyevent 61") #back
        found = a.find(a.i.export2, region=r, grayscale=True)
        if found:
            x = found.found[0] #- w.topleft.x
            y = found.found[1] #- w.topleft.y
            adb(f'input tap {x} {y}')
            return
        time.sleep(1)

    logging.debug(f"Failed to find export button after pressing tab 20 times")


#find either the button to open export menu("export") or 
# the final first line export video text("export tovideo file")
found = a.find([a.i.export_to_video_file, a.i.export], loop=3, region=r, grayscale=True)
if found:
    if  found == a.i.export_to_video_file:
        adb(f"input keyevent 4") #back
    found = a.find([a.i.export], loop=3, region=r, grayscale=True)
    if found:
        adb(f'input tap {found.found[0]} {found.found[1]}')
#    else:
#scroll to find final export button
tab_scroll() 

#wait for encode to finish and click the ad cross button
found = a.find([a.i.export, a.i.ad_cross], loop=5, timeout=5*60, region=r, grayscale=True)
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
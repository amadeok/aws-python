import win32gui,pywintypes
import win32con,win32file,win32pipe,win32api, numpy
import pygetwindow as gw
import time, subprocess as sp, mss
from PIL import Image
import logging
# time.sleep(1)

import win32gui
import win32ui
import random
import autopy as at
from autopy import background_screenshot
import urllib.parse

import time
import pywinauto, ctypes, os
from urllib.parse import quote
from collections import namedtuple

a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"

w = gw.getWindowsWithTitle("LDPlayer")[0]
hwnd = win32gui.FindWindow(None, "LDPlayer")


def is_avee_running():
    process = sp.Popen("adb shell pidof com.daaw.avee",
                        shell=True,
                           stdout=sp.PIPE, 
                           stderr=sp.PIPE)

    out, err = process.communicate()
    errcode = process.returncode
    if out != b'':
        return True
    return False
    
def check_avee_running():
    
    if not is_avee_running():
        logging.debug("Avee not running, starting")
        os.system(f"{base} am start -a android.intent.action.VIEW -n com.daaw.avee/.MainActivity")
        ret = a.find(a.i.dict[prefix + "speaker"], loop=3, region=r)
        time.sleep(4)
    else:
        logging.debug("Avee running")
    
wid = 720 
hei = 1280

background_screenshot(hwnd, wid, hei+52,True)

r = (w.topleft.x, w.topleft.y, wid, w.height)

prefix = "720p_"
template_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\AveeTemplate_normal\\"
audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"

nt = namedtuple("name_storage", "android_name win_name")

template_list = [nt(quote(elem), elem) for elem in os.listdir(template_fld)]
audio_list = [nt(quote(elem), elem) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

a = at.autopy("images_avee", w._hWnd)
base = "adb  -s emulator-5554 shell "

file = "file:///mnt/shared/Pictures/" + random.choice(audio_list).android_name #00024.wav"
file_cmd = f'{base} am start -a android.intent.action.VIEW -d "{file}" -n com.daaw.avee/.MainActivity'

temp_file = "file:///mnt/shared/Pictures/AveeTemplate_normal/" + random.choice(template_list).android_name # CX%20liquify.viz"
temp_cmd = f'{base} am start -a android.intent.action.VIEW -d "{temp_file}" -n com.daaw.avee/.MainActivity'

sleep_t = 4
os.system("adb start-server ")
os.system("adb start-server ")
check_avee_running()

found = a.find(a.i.dict[prefix + "ad_cross"], region=r, grayscale=True)
if found:
    x = found.found[0] - w.topleft.x
    y = found.found[1] - w.topleft.y

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
        os.system(f"adb  -s emulator-5554 shell input keyevent 61") #back
        found = a.find(a.i.dict[prefix + "export2"], region=r, grayscale=True)
        if found:
            x = found.found[0] - w.topleft.x
            y = found.found[1] - w.topleft.y
            os.system(f'adb  -s emulator-5554 shell input tap {x} {y}')
            return
        time.sleep(1)

    logging.debug(f"Failed to find export button after pressing tab 20 times")



found = a.find([a.i.dict[prefix + "export"], a.i.dict[prefix + "export_to_video_file" ]], region=r, grayscale=True)
if found and  found == a.i.dict[prefix + "export"]:
    x = found.found[0] - w.topleft.x
    y = found.found[1] - w.topleft.y
    os.system(f'adb  -s emulator-5554 shell input tap {x} {y}')

tab_scroll()
#ret = a.find(a.i.dict[prefix + "export_to_video_file"], loop=3, region=r, grayscale=True)

os.system(f"adb  -s emulator-5554 shell input keyevent 4") #back

#os.system(f'adb  -s emulator-5554 shell  am broadcast -a com.llamalab.automate.intent.action.START_FLOW -d content://com.llamalab.automate.provider/flows/8/statements/1 -n com.llamalab.automate/.StartServiceReceiver -e Payload "x{x_perc}x{y_perc}"')



# print(time.time() - t0)
# output_pipe =  r'\\.\pipe\dain_a_id' 
# input_pipe =  r'\\.\pipe\dain_b_id'
# mode = win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT
# fd0 = win32pipe.CreateNamedPipe( output_pipe, win32pipe.PIPE_ACCESS_DUPLEX, mode, 1, 65536, 65536, 0, None)
# ret = win32pipe.ConnectNamedPipe(fd0, None)
# if ret != 0:
#     print("error fd0", win32api.GetLastError())
# print(f'Python capture ID : Output pipe opened')

# w = 1080
# h = 1920
# s = 3
# tot_data = b''
# arr = bytearray(w*h*s)
# pos = 0
# buffer_size= 20480
# t0 = time.time()
# # while 1:
#     try:
#         data = win32file.ReadFile(fd0, buffer_size) #w*h*s
#     except:
#         break
#     lenght_read = len(data[1])
#     arr[pos:pos+lenght_read] = data[1]
#     pos+=lenght_read
#     #tot_data+=data[1]
#     if not data:
#         break

# print(time.time() -t0)

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
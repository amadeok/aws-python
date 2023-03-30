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

import time, shlex
import pywinauto, ctypes, os,win32process
from urllib.parse import quote
from collections import namedtuple

#!/usr/bin/env python

a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"


def restart_ld_player(hwnd=None):
    # if hwnd:
    #     threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    #     os.system(f"taskkill /PID {pid}")
    #     time.sleep(0.5)
    # process = sp.Popen(r"F:\LDPlayer\LDPlayer9\dnplayer.exe")
    # ldplayer_pid = process.pid
    # time.sleep(1)
    ld_win = gw.getWindowsWithTitle("LDPlayer")[0]
    hwnd = ld_win._hWnd

    return hwnd, ld_win
hwnd, ld_win= restart_ld_player(hwnd = None )

ld_win = gw.getWindowsWithTitle("LDPlayer")[0]
hwnd = ld_win._hWnd
ldplayer_pid = None


def adb_output(cmd):
    process = sp.Popen(base + cmd,
                        shell=True,
                           stdout=sp.PIPE, 
                           stderr=sp.PIPE)

    out, err = process.communicate()
    errcode = process.returncode
    return out if len(out) else err

def is_avee_running():
    ret =  adb_output(f"pidof com.daaw.avee")
    if ret != b'':
        return True
    return False
    
def check_avee_running():
    
    if not is_avee_running():
        logging.debug("Avee not running, starting")
        os.system(f"{base} am start -a android.intent.action.VIEW -n com.daaw.avee/.MainActivity")
        ret = a.find(a.i.speaker, timeout=40, loop=3, region=r)
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

def is_device_ready():
    ret = adb_output("qwx")
    if "'emulator-5554' not found" in str(ret):
        return False
    return True

def wait_for_device():
    while not is_device_ready():
        print("device not ready..")
        time.sleep(1)
    os.system("adb start-server ")
    os.system("adb start-server ")





wid = 540 
hei = 960 +50

device = "ce041714f506223101" # emulator-5554
device = "emulator-5554"

base = f"adb  -s {device} shell "



background_screenshot(hwnd, wid, hei+52,True)
#ret = receive_screen_shot_from_phone(save_file=True)

#check_device_awake()

r = (ld_win.topleft.x, ld_win.topleft.y, wid, hei)

def xcoor(x):
    xx = x - ld_win.topleft.x
    return xx
def ycoor(y):
    yy = y - ld_win.topleft.y
    return yy


prefix = "540p_"
template_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\AveeTemplate_normal\\"
audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"

nt = namedtuple("name_storage", "android_name win_name")

template_list = [nt(quote(elem), elem) for elem in os.listdir(template_fld)]
audio_list = [nt(quote(elem), elem) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

a = at.autopy("images_avee", ext_src=hwnd, img_prefix=prefix) #w._hWnd
a.ext_src_buffer =  bytearray(wid*hei*3)
# target_file = nt("", "")
# while not "(" in target_file.win_name:
target_file =  random.choice(audio_list)



andr_input_fld = "/mnt/shared/Pictures/"

#target_file = nt(quote("s.mp3"), "s.mp3")# random.choice(audio_list)
file = "/mnt/shared/Pictures/" + target_file.android_name #DO NOT USE THIS FOLDER, IT CRASHES ENCODING  #file = "file:///mnt/shared/Pictures/" + random.choice(audio_list).android_name #00024.wav"
new_name_spl =  target_file.win_name.split(".")
new_name = new_name_spl[0] + "_new_." + new_name_spl[1]
new_name = new_name.replace("(", "_")
new_name = new_name.replace(")", "_")
ex_file = "00000.mp3" if "mp3" in new_name else "00001.wav"


file = "file:///mnt/shared/Pictures/" + ex_file# quote(new_name)
file_cmd = f'{base} am start -a android.intent.action.VIEW -d "{file}" -n com.daaw.avee/.MainActivity'

temp_file = "file:///mnt/sdcard/input/templates/AveeTemplate_normal/" + random.choice(template_list).android_name # CX%20liquify.viz"
temp_file = "file:///mnt/shared/Pictures/AveeTemplate_normal/" + random.choice(template_list).android_name # CX%20liquify.viz"
temp_cmd = f'{base} am start -a android.intent.action.VIEW -d "{temp_file}" -n com.daaw.avee/.MainActivity'

sleep_t = 2
os.system("adb start-server ")
os.system("adb start-server ")
adb("mkdir /mnt/shared/Pictures/input ")
adb("mkdir /mnt/shared/Pictures/input/audio ")
adb("mkdir /mnt/shared/Pictures/input/templates")
try: os.mkdir("tmp")
except: pass

os.system(f"ffmpeg -i {audio_fld +  target_file.win_name } -s 0 -to 15 tmp\\{new_name} -y")
adb("mkdir /mnt/sdcard/Pictures/output ")


wait_for_device()
cmd = f'adb -s {device} push ' +  "tmp\\"+ new_name   + (' /mnt/shared/Pictures/' +shlex.quote(ex_file))
print("####->", cmd)
os.system(cmd)

hwnd, ld_win= restart_ld_player(hwnd)
wait_for_device()
a.ext_src = hwnd
r = (ld_win.topleft.x, ld_win.topleft.y, wid, hei)
p = None
f = open(p, "wb")

#found = a.find(a.i.play_store, loop=3, timeout=30, region=r, grayscale=True)


#adb("cp " + audio_fld.replace("\\", "/") + file2.win_name +  " /mnt/sdcard/input" )


# while is_avee_running():
#     adb(f"input keyevent 4") #back
#     time.sleep(0.5)
adb("am force-stop com.daaw.avee")

check_avee_running()

# found = a.find(a.i.ad_cross, region=r, grayscale=True)
# if found:
#     x = found.found[0]# - w.topleft.x
#     y = found.found[1]# - w.topleft.y
#     adb(f'input tap {x} {y}')

time.sleep(sleep_t)

found = a.find([a.i.export_to_video_file, a.i.export2], timeout=7, loop=3, region=r, grayscale=True)
if found:
    adb(f"input keyevent 4") #back


check_avee_running()
os.system(file_cmd)
ret = a.find(a.i.pause, timeout=15, loop=3, region=r)
adb(f'input tap {xcoor(ret.found[0])} {ycoor(ret.found[1])}')
time.sleep(sleep_t)

check_avee_running()
os.system(temp_cmd)
time.sleep(sleep_t)

t0 = None

def tab_scroll():
    global t0
    logging.debug(f"Tab scrolling ")

    found = a.find(a.i.file_name, loop=6, region=r, grayscale=True)
    x =xcoor(found.found[0]+141)
    y = ycoor(found.found[1])
    cmd = f'"input tap {x} {y}& sleep 0.1; input tap {x} {y}"'
    adb(cmd)
    time.sleep(0.6)

    cmd = "input text " + f'{shlex.quote(target_file.win_name.split(".")[0])}'
    adb(cmd)


    found = None
    for x in range(20):
        adb(f" input keyevent 61") #back
        found = a.find(a.i.export2, region=r, grayscale=True)
        if found:
            adb(f'input tap {xcoor(found.found[0])} {ycoor(found.found[1])}')
            t0 = time.time()
            return
        time.sleep(0.1)

    logging.debug(f"Failed to find export button after pressing tab 20 times")


#find either the button to open export menu("export") or 
# the final first line export video text("export tovideo file")
found = a.find([a.i.export_to_video_file, a.i.export], timeout=40, loop=3, region=r, grayscale=True)
if found:
    if  found == a.i.export_to_video_file:
        adb(f"input keyevent 4") #back
    found = a.find([a.i.export], loop=3, region=r, grayscale=True)
    if found:
        adb(f'input tap  {xcoor(found.found[0])} {ycoor(found.found[1])}')
#    else:
#scroll to find final export button
adb('"cd /mnt/sdcard/Download && rm -rf *.mp4"')
tab_scroll() 
found = a.find([a.i.blue_cross], loop=3, region=r, grayscale=True)

#wait for encode to finish and click the ad cross button
found = a.find([a.i.exporting_finished, a.i.export2], loop=5, timeout=5*60, region=r, grayscale=True)
print("encode took aprox", time.time() - t0)
ex_file_spl =  ex_file.split(".")

cmd = "mv " + f'"/mnt/sdcard/Download/{shlex.quote(new_name_spl[0])}_0.mp4"' +  " /mnt/shared/Pictures/output/"+ shlex.quote(new_name_spl[0]) + ".mp4" 
adb(cmd)

if found: #and  
    if found == a.i.exporting_finished:
        time.sleep(1)
        adb(f" input keyevent 61") #back
        adb(f'input tap  {xcoor(found.found[0]) +240 } {ycoor(found.found[1] + 158)}')

    adb(f'input tap  {440} {610}')








#ret = a.find(a.i.dict[prefix + "export_to_video_file"], loop=3, region=r, grayscale=True)

os.system(f"a58db  -s emulator-5554 shell input keyevent 4") #back

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
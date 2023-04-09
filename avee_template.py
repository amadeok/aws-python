import pygetwindow as gw
import time, subprocess as sp, mss
from PIL import Image
import logging, math
# time.sleep(1)

import win32gui
import win32ui
import random, traceback
import autopy as at
from autopy import background_screenshot, receive_screen_shot_from_phone

import time, shlex, random, numpy as np
import pywinauto, ctypes, os,win32process
from urllib.parse import quote
from collections import namedtuple
import seaborn as sns, webcolors

#!/usr/bin/env python

from avee_utils import *

#a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"

#background_screenshot(hwnd, wid, hei+52,True)
#ret = receive_screen_shot_from_phone(save_file=True)

#check_device_awake()



template_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\AveeTemplate_normal\\"
audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"
fonts = ['Open Sans', 'Arial Rounded MT Bold', 'Bauhaus 93', 'Berlin Sans FB', 'Cambria Math', 'Comic Sans MS', 'Eras Bold ITC', 'Eras Demi ITC', 'Gill Sans Ultra Bold Condensed', 'Harrington', 'High Tower Text', 'Imprint MT Shadow', 'Jokerman', 'Kristen ITC',"Maiandra GD","Matura MT Script Capitals","MS PGothic","MV Boli","Trebuchet MS","Tw Cen MT","Tw Cen MT Condensed Extra Bold","Ubuntu","Open Sans"]

nt = namedtuple("name_storage", "android_name win_name basename dirpath")

template_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(template_fld)]
audio_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

andr_input_fld = "/mnt/shared/Pictures/"


f = "00032.mp3"
#f = random.choice(os.listdir(audio_fld))
input_file = audio_fld + "//" + f

#temp_file = "file:///mnt/sdcard/input/templates/AveeTemplate_normal/" + random.choice(template_list).android_name # CX%20liquify.viz"
#target_file =  random.choice(audio_list)
template =  "The fuzzy lear.viz"#random.choice(template_list).win_name 


try: os.mkdir("tmp")
except: pass

out = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\\"


os.system("adb start-server ")
os.system("adb start-server ")

template = random.choice(template_list).win_name 

template_file_path = "file:///mnt/shared/Pictures/AveeTemplate_normal/" + shlex.quote(template) # CX%20liquify.viz"

template_cmd = f'{base} am start -a android.intent.action.VIEW -d "{template_file_path}" -n com.daaw.avee/.MainActivity'

from pynput.keyboard import Key, Listener

text = ""
#template_ = ""
template_index = 0

def templ_cmd(templ):
    template_file_path = "file:///mnt/shared/Pictures/AveeTemplate_normal/" + shlex.quote(templ.win_name) # CX%20liquify.viz"
    return f'am start -a android.intent.action.VIEW -d "{template_file_path}" -n com.daaw.avee/.MainActivity'

def find_template():
    global text; global template_; global template_index
    for i, t in enumerate(template_list):
        if text.lower() in t.win_name.lower():
 #           template_ = t
            template_index = i
            print(f"found template n {i}: {t.win_name}")

def on_press(key):
    global text; global template_index 
    #print('{0} pressed'.format(
    #    key))
    try:
        if key.char == "+": 
            template_index +=1 
            if template_index >= len(template_list):
                template_index = len(template_list)-1
            print(f"###### selected template n {template_index}: {template_list[template_index].win_name}")
            print("++")
            adb(templ_cmd(template_list[template_index]))
        if key.char == "-": 
            template_index -=1 
            if template_index < 0:
                template_index = 0
            print(f"###### selected template n {template_index}: {template_list[template_index].win_name}")
            print("--")
            adb(templ_cmd(template_list[template_index]))


    except Exception as e:
        if key.name == "f3":
            text = "!!!"
        print(e)


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def lis(): # Collect events until released
    with Listener(
            on_press=on_press,
            #on_release=on_release
            ) as listener:
        listener.join()

t= threading.Thread(target=lis)
t.start()

adb("am force-stop com.daaw.avee")
time.sleep(0.5)
reset_settings()
# settings_f = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\shared_prefs"
# for f in os.listdir(settings_f):
#     bb = "adb  -s emulator-5554 shell" + f" su -c 'cp /storage/emulated/0/Pictures/shared_prefs/{f} /data/data/com.daaw.avee/shared_prefs;'"
#     os.system(bb)

while 1:
    time.sleep(1)
    if text == "!!!":
        print("enter new text: ")
        text = input()[:]
        print(f"new text ...{text}...")
        find_template()
        adb(templ_cmd(template_list[template_index]))

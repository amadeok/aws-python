import tempfile
import win32con,win32file,win32pipe,win32api, numpy, threading
import pygetwindow as gw
import time, subprocess as sp, mss, os
from PIL import Image
import logging, math, shutil
import random, traceback, queue
# import autopy as at
# from autopy import background_screenshot, receive_screen_shot_from_phone
import time, shlex, random, numpy as np
from urllib.parse import quote
from collections import namedtuple
import seaborn as sns            
from avee_utils import *
import dav, app_logging
from configparser import ConfigParser
import sql_utils
from base import *
import app_env
import pyautogui
import pyscreeze
import utils.process_videos as pv


print("pyautogui version:", pyautogui.__version__)
print("pyscreeze version:", pyscreeze.__version__)

audio_fld = f"{app_env.audio_folder}\\"

#nt = namedtuple("name_storage", "android_name win_name basename dirpath")
#audio_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

#f = "00002(5).wav"
#f = "00019v2_s.wav"
f = "00024v2_s.wav"
#f = "00039.wav"
#f = random.choice(os.listdir(audio_fld))
input_file_ = audio_fld + "//" + f
input_file_ = r"C:\Users\%USERNAME%\Downloads\00001 Forest Walk short.wav"#r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\00025_s.wav"#

input_file_ = input_file_.replace("%USERNAME%", os.getenv("USERNAME"))

#input_file_ = r"C:\Users\amade\Documents\dawd\Exported\00034\Mixdown\s_00034(5).wav"
#input_file_ = f"{app_env.ld_shared_folder}\v2\00028v2.wav"

# if not os.path.isfile(input_file_) or not os.path.isfile(input_file_.split(".")[0] + ".ini"):
#     raise Exception("input files not found")

if not os.path.isdir("tmp"): os.mkdir("tmp")
if not os.path.isdir("vis"): os.mkdir("vis")

sql = sql_utils.sql_()
rows = []
for  row in sql.cur.execute('''SELECT * FROM Main '''):
    rows.append(row)

fr_l = [n+5 for n in range(len(rows))]; assert (not 0 in fr_l) #len(rows)//2 
random.shuffle(fr_l)
multithread = False
#rows  = [sql.get_row("rom0!")]


def main_aws(do_aws=1):
    threads = []
    if multithread:
        threads.append(threading.Thread(target=avee_worker, args=(rows, input_file_, fr_l)))
        threads.append(threading.Thread(target=dav_worker, args=()))
        if do_aws: threads.append(threading.Thread(target=aws_worker, args=()))
        for tt in threads:
            tt.start()
        for tt in threads:
            tt.join()
        #to fix the wrong "end at" bug in avee
        os.system("adb -s emulator-5554 push "+  f"{app_env.ld_shared_folder}\00034.wav" + " /mnt/sdcard/Pictures/00001.wav")
        
    else:
        for  i, row in enumerate(rows):
            general_task_aws(row[3], input_file_, sql, fr_l[i], do_aws)

import base
def main(upload=False):
    custom_vi = os.path.expanduser('~') + r"\Videos\social_media_videos\horizontal\ai_rain__4088192-hd_1920_1080_25fps.mp4"
    custom_vi = os.path.expanduser('~') + r"Videos\social_media_videos\horizontal\202004\ai_restaurant_cafe__202004-916894674.mp4"#os.path.expanduser('~') +"Videos\social_media_videos\vertical\sakura_trees_pink_stairs__156010-811683620.mp4"
    custom_vi = os.path.expanduser('~') + r"Videos\social_media_videos\vertical\mountains_forest__198802-908900247.mp4"
    custom_vi = random.choice(pv.get_sm_videos())
    
    base.general_task(input_file_,  fr_l[0], add_text=True, custom_video=custom_vi, secondary_text="peaceful_piano_music")

main(upload=0)
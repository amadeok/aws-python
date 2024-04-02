import win32con,win32file,win32pipe,win32api, numpy, threading
import pygetwindow as gw
import time, subprocess as sp, mss, os
from PIL import Image
import logging, math, shutil
import random, traceback, queue
import autopy as at
from autopy import background_screenshot, receive_screen_shot_from_phone
import time, shlex, random, numpy as np
from urllib.parse import quote
from collections import namedtuple
import seaborn as sns            
from avee_utils import *
import dav, app_logging
from configparser import ConfigParser
import sql_utils
from base import *

audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"

#nt = namedtuple("name_storage", "android_name win_name basename dirpath")
#audio_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

#f = "00002(5).wav"
#f = "00019v2_s.wav"
#f = "00024v2_s.wav"
f = "00039.wav"
#f = random.choice(os.listdir(audio_fld))
input_file_ = audio_fld + "//" + f
#input_file_ = r"C:\Users\amade\Documents\dawd\Exported\00034\Mixdown\s_00034(5).wav"
#input_file_ = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\v2\00028v2.wav"

if not os.path.isfile(input_file_) or not os.path.isfile(input_file_.split(".")[0] + ".ini"):
    raise Exception("input files not found")

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
        os.system("adb -s emulator-5554 push "+  r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\00034.wav" + " /mnt/sdcard/Pictures/00001.wav")
        
    else:
        for  i, row in enumerate(rows):
            general_task_aws(row[3], input_file_, sql, fr_l[i], do_aws)

def main(upload=False):
    general_task(input_file_,  fr_l[0], add_text=True)

main(upload=0)
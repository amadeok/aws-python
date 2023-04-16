import webcolors
import win32gui,pywintypes
import win32con,win32file,win32pipe,win32api, numpy, threading
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
import urllib.parse

import time, shlex, random, numpy as np
import pywinauto, ctypes, os,win32process
from urllib.parse import quote
from collections import namedtuple
import seaborn as sns

from avee_utils import *
import dav

audio_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\\"

nt = namedtuple("name_storage", "android_name win_name basename dirpath")

audio_list = [nt(shlex.quote(elem), elem, elem.split(".")[0], os.path.dirname(elem) ) for elem in os.listdir(audio_fld) if ".wav" in elem or ".mp3" in elem]

f = "00002(5).wav"
#f = random.choice(os.listdir(audio_fld))
input_file = audio_fld + "//" + f

if not os.path.isdir("tmp"): os.mkdir("tmp")

class context():
    def __init__(s) -> None:

        s.bpm = 80
        s.s_m = 0
        s.s_sec = 50
        s.s_ms = 743
        s.bars=8
        s.bars_per_template=1
        s.beats_per_bar = 4
        s.out_fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\\"
        s.input_f = name_storage(input_file,  s.out_fld)
        s.fps = 60 #59940/1000
        s.time_per_beat = (60/s.bpm)
        s.frames_per_beat = s.fps * s.time_per_beat
        s.frames_per_bar = s.frames_per_beat * s.beats_per_bar
        s.transition_delta = s.frames_per_bar * s.bars_per_template
        s.tot_transitions = s.bars // s.bars_per_template

ctx = context()

perform_avee_task(ctx.input_f, ctx.bpm, (ctx.s_m, ctx.s_sec, ctx.s_ms), ctx.bars, ctx.bars_per_template, beats_per_bar=ctx.beats_per_bar)

davinci = dav.dav_handler(ctx)



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

import time, shlex
import pywinauto, ctypes, os,win32process
from urllib.parse import quote
from collections import namedtuple

#a = r"C:\Program Files\WindowsApps\11314DaawAww.AveePlayer_0.8.25.0_x64__3mhsykt1m20fj\BleuPlayer.UWP.exe"
#nt = namedtuple("name_storage", "android_name win_name basename dirpath")

class name_storage():
    def __init__(self, input_path, out) -> None:
        self.input_path = input_path
        self.win_name = os.path.basename(input_path)
        self.android_name = shlex.quote(self.win_name)
        self.basename =  self.win_name.split(".")[0]
        self.android_basename =  shlex.quote(self.basename)
        self.dirpath = os.path.dirname(input_path)
        self.out_fld = f"{out}\\{self.basename}\\".replace("\\\\", "\\")
        self.avee_final_file = f"{self.out_fld}\\{self.basename}_joined.mp4".replace("\\\\", "\\")

device = "ce041714f506223101" # emulator-5554
device = "emulator-5554"

base = f"adb  -s {device} shell "

ctx = None





def restart_ld_player(hwnd=None):
    # if hwnd:
    #     threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    #     os.system(f"taskkill /PID {pid}")
    #     time.sleep(0.5)
    # process = sp.Popen(r"F:\LDPlayer\LDPlayer9\dnplayer.exe")
    # ldplayer_pid = process.pid
    # time.sleep(1)
    l = gw.getWindowsWithTitle("LDPlayer")
    while len(l) == 0:
        l = gw.getWindowsWithTitle("LDPlayer")
        logging.info("waiting for lplayer..")
        time.sleep(1)
    ld_win = l[0]
    hwnd = ld_win._hWnd

    return hwnd, ld_win

# exe = r"F:\LDPlayer\LDPlayer9\dnplayer.exe"
# command = ['schtasks', '/run', '/tn', exe]
# sp.Popen(["cmd.exe", '/c', 'start']+command)

#hwnd, ld_win= restart_ld_player(hwnd = None )

class context():
    def __init__(s, wid, hei, prefix, autopy=None) -> None:
        s.wid = wid
        s.hei = hei
        s.hwnd, s.ld_win= restart_ld_player(hwnd = None )
        s.r = (s.ld_win.topleft.x, s.ld_win.topleft.y, s.wid, s.hei)
        s.prefix = prefix
        s.a = autopy if autopy else at.autopy("images_avee", ext_src=s.hwnd, img_prefix=s.prefix) #w._hWnd

    def xcoor(s, x):
        xx = x - s.ld_win.topleft.x
        return xx
    def ycoor(s, y):
        yy = y - s.ld_win.topleft.y
        return yy


# wid = 540 
# hei = 960 +50
# r = (ld_win.topleft.x, ld_win.topleft.y, wid, hei)





#a.ext_src_buffer =  bytearray(wid*hei*3)


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
    global ctx
    if not is_avee_running():
        logging.debug("Avee not running, starting")
        os.system(f"{base} am start -a android.intent.action.VIEW -n com.daaw.avee/.MainActivity")
        ret = ctx.a.find(ctx.a.i.speaker, timeout=40, loop=3, region=ctx.r, check_avee_running=False)
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


def tab_scroll(target_file, suffix):
    global t0; global ctx
    logging.debug(f"Tab scrolling ")

    found = ctx.a.find(ctx.a.i.file_name, loop=6, region=ctx.r, grayscale=True)
    x =ctx.xcoor(found.found[0]+141)
    y = ctx.ycoor(found.found[1])
    cmd = f'"input tap {x} {y}& sleep 0.1; input tap {x} {y}"'
    adb(cmd)
    time.sleep(0.6)

    cmd = "input text " + f'{shlex.quote(f"{target_file.basename}_{suffix:02d}" )}'
    adb(cmd)


    found = None
    for x in range(20):
        adb(f" input keyevent 61") #back
        found = ctx.a.find(ctx.a.i.export2, region=ctx.r, grayscale=True)
        if found:
            adb(f'input tap {ctx.xcoor(found.found[0])} {ctx.ycoor(found.found[1])}')
            t0 = time.time()
            return
        time.sleep(0.1)

    logging.debug(f"Failed to find export button after pressing tab 20 times")



def avee_task(target_file, template_file, start, dur, suffix):
    global ctx
    os.system("adb start-server ")
    os.system("adb start-server ")
    adb("mkdir /mnt/sdcard/Pictures/output ")
    adb("mkdir /mnt/shared/Pictures/input ")
    adb("mkdir /mnt/shared/Pictures/input/audio ")
    adb("mkdir /mnt/shared/Pictures/input/templates")

    ctx = context(hei= 960+50, wid=540, prefix="540p_", autopy=None)
    a = ctx.a

    sleep_t = 2

    #target_file =  nt(shlex.quote(basef),basef, basef.split(".")[0], os.path.dirname(basef))

    os.system(f"ffmpeg -i {target_file.input_path } -ss {start} -t {dur} tmp\\{target_file.win_name} -y")
    
   
    file = "/mnt/shared/Pictures/" + target_file.android_name #file = "file:///mnt/shared/Pictures/" + random.choice(audio_list).android_name #00024.wav"
    #new_name_spl =  target_file.win_name.split(".")
    #new_name = new_name_spl[0] + "_new_." + new_name_spl[1]
    ex_file = "00000.mp3" if "mp3" in file else "00001.wav"
    file = "file:///mnt/shared/Pictures/" + ex_file# quote(new_name)

    file_cmd = f'{base} am start -a android.intent.action.VIEW -d "{file}" -n com.daaw.avee/.MainActivity'

    template_file_path = "file:///mnt/shared/Pictures/AveeTemplate_normal/" + shlex.quote(template_file) # CX%20liquify.viz"
    template_cmd = f'{base} am start -a android.intent.action.VIEW -d "{template_file_path}" -n com.daaw.avee/.MainActivity'

    wait_for_device()

    cmd = f'adb -s {device} push ' +  "tmp\\"+ target_file.win_name   + (' /mnt/sdcard/Pictures/' +shlex.quote(ex_file))
    #print("####->", cmd)
    os.system(cmd)

    ctx.hwnd, ctx.ld_win= restart_ld_player()
    wait_for_device()
    ctx.a.ext_src = ctx.hwnd
    r = (ctx.ld_win.topleft.x, ctx.ld_win.topleft.y, ctx.wid, ctx.hei)

    adb("am force-stop com.daaw.avee")
    time.sleep(1)
    check_avee_running()

    time.sleep(sleep_t)

    check_avee_running()
    os.system(file_cmd)
    ret = a.find(a.i.pause, timeout=15, loop=0.5, region=r)
    adb(f'input tap {ctx.xcoor(ret.found[0])} {ctx.ycoor(ret.found[1])}')
    time.sleep(sleep_t)

    check_avee_running()
    os.system(template_cmd)
    time.sleep(sleep_t)
    
    if not is_avee_running():
        logging.info(f" template crash? {template_file}")
    t0 = time.time()

    #find either the button to open export menu("export") or 
    # the final first line export video text("export tovideo file")
    found = a.find([a.i.export_to_video_file, a.i.export], timeout=40, loop=1, region=r, grayscale=True)
    if found:
        if  found == a.i.export_to_video_file:
            adb(f"input keyevent 4") #back
        found = a.find([a.i.export], loop=1, region=r, grayscale=True)
        if found:
            adb(f'input tap  {ctx.xcoor(found.found[0])} {ctx.ycoor(found.found[1])}')
    #    else:
    #scroll to find final export button
    adb('"cd /mnt/sdcard/Download && rm -rf *.mp4"')
    tab_scroll(target_file, suffix)

    found = a.find([a.i.blue_cross], loop=1, region=r, grayscale=True)

    #wait for encode to finish and click the ad cross button
    found = a.find([a.i.exporting_finished, a.i.export2], loop=5, timeout=5*60, region=r, grayscale=True)
    logging.info(f"encode took aprox {time.time() - t0}secs")
    ex_file_spl =  ex_file.split(".")

    adb(f"mkdir /mnt/shared/Pictures/output/{target_file.android_basename }/ ")
    adb(f"mkdir /mnt/shared/Pictures/output/{target_file.android_basename }/tmp ")
    cmd = "mv " + f'"/mnt/sdcard/Download/{target_file.android_basename }_{suffix:02d}_0.mp4"' +  f" /mnt/shared/Pictures/output/{target_file.android_basename }/tmp/"+ target_file.android_basename  + f"_{suffix:02d}.mp4" 
    adb(cmd)

    if found: #and  
        if found == a.i.exporting_finished:
            time.sleep(1)
            adb(f" input keyevent 61") #back
            adb(f'input tap  {ctx.xcoor(found.found[0]) +240 } {ctx.ycoor(found.found[1] + 158)}')

        adb(f'input tap  {440} {610}')
import os, subprocess as sp
import time
import socket
import atexit
import select
import pyautogui as pg
import autopy as at
import os
import network
print(os.getcwd())
import os, platform
from datetime import datetime
import distro
import logging
import app_logging
import traceback
import shutil, keyboard
from pathlib import Path
from pyKey import pressKey, releaseKey, press, sendSequence, showKeys

prefix = "70p_"
print(pg._pyautogui_x11.keyboardMapping)

#time.sleep(3)
# for elem in pg._pyautogui_x11.keyboardMapping:
#     #sendSequence(elem)
#     #sendSequence(" || ")
#     pg.write(f"'{elem}' " ) 
#     pg.write(elem)
#     pg.write("\n")
#     #sendSequence("\n")
#     time.sleep(0.1)#pop

a = at.autopy("images", img_prefix=prefix)

print(os.getcwd())
print(distro.info())

home = "amadeok" if app_logging.ubuntu_ver =="20.04" else "ubuntu"
with open(f"/home/{home}/f.txt",  "w") as ww:
    ww.write(str(datetime.now().strftime("%H:%M:%S")) )

REM_HOST = "0.0.0.0"
REM_PORT = 4003

# HOST = '192.168.1.230'  # Standard loopback interface address (localhost)
# PORT = 9595

#exit()
suffix = "_o"

def browse_task():
    cmd = ["firefox", "https://www.tiktok.com/upload?lang=en", "--display=:1"]
    p = sp.Popen(cmd)

    time.sleep(2)
    handles = []
    while 1:
        cmd2 = [f"xdotool", "search", "--name", str("Firefox")]
        p2 = sp.Popen(cmd2, stdout=sp.PIPE)
        out, err = p2.communicate()
        handles = str(out.decode("utf-8")).split("\n")
        if len(out) >= 3:
            break
        a.rlog("waiting for firefox..")
        time.sleep(0.5)
    
#        os.system("xdotool  windowsize 100% 50%")

    os.system("wmctrl -r Firedox -b remove,maximized_vert,maximized_horz")
    for w in handles:
        os.system(f"xdotool   windowmove {w} 0 0 ")
        os.system(f"xdotool   windowsize {w} 1280 1024 ")

    #os.system(f"wmctrl -r Firedox -e 0,1300,45,1630,940")

  #  xdotool Firefox getwindowgeometry --shell
    ret = a.find(a.i.tiktok_logo, loop=2,timeout=80, timeout_exception="tiktok page didn't open")

    if a.find(a.i.login_to_tiktok, loop=1,timeout=5):
        raise Exception("tiktok is requesting login")
            
    ret = a.find(a.i.select_file, loop=2, timeout_exception=True)
    a.click(ret.found, 140, -232)  
    time.sleep(0.5)
    a.type("#pop")
    a.click(ret.found, 0, 0)  

    a.find(a.i.dict["open_file" + suffix], loop=2, timeout_exception=True)
    a.press("enter")
    a.find(a.i.post, loop=2, timeout_exception=True, click=1)



    if ret:
        for x in range(2):
            a.click(ret.found, 0, 0)  
            #a.click(ret.found, 140, -232)  
            time.sleep(100.5)
        a.type("#pop")
        time.sleep(1)
        a.press("enter")

            #network.send_string(message + str(x), conn)
    a.rlog("closing connection.. ", conn=conn)

if __name__ == '__main__':
    import sys
    port = 9001
    print("lisetining at " + REM_HOST + ":" + str(REM_PORT))

    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    while 1:
        try:
            s.bind((REM_HOST, REM_PORT))
            s.listen()
            conn, addr = s.accept()
            print("Socket connected " + addr[0] + ":" + str(addr[1]))
            break
              

        except Exception as e:
            print(e)
            time.sleep(1)
            #conn.close()

    upload_fld = os.path.expanduser('~') + "/Desktop"

    dirpath =  Path(upload_fld + "/Old Firefox Data"  ) 
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)


    prefix = "70p_"
    a = at.autopy("images", img_prefix=prefix)
    a.conn = conn

    network.recveive_file(upload_fld +  "/file.mp4", conn)
    
    try:
        browse_task()
    except Exception as e:
        a.rlog("Exception: " + traceback.format_exc())
        a.rlog("Exception: " + str(e))

    conn.close()

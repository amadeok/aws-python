import logging, time, traceback
while 1:
    try:
        import pyautogui as pg
        break
    except Exception as e:
        print(f"Failed to import pyautogui: {traceback.format_exc()} \n Exception: {e}")
        time.sleep(1)
import app_logging
import os, subprocess as sp
from time import sleep
import socket
#import atexit
#import select
import autopy as at
import os
import network
print(os.getcwd())
import os, platform
from datetime import datetime
import distro
import logging
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
suffix = "_o" if app_logging.ubuntu_ver == "20.04" else ""
del_ = at.fun_delegate

def type_hashtags(select_file, hashtags):
    a.click(select_file.found, 140, -232)  
    time.sleep(0.5)
    a.type(hashtags)
    time.sleep(0.5)

def start_firefox(url):
    os.system("pkill firefox")
    sleep(0.5)

    cmd = ["firefox", url, "--display=:1"]
    p = sp.Popen(cmd)

    sleep(2)
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

def browse_task(yt_id):
    
    #os.system(f"wmctrl -r Firedox -e 0,1300,45,1630,940")
    tiktok_url = "https://www.tiktok.com/upload?lang=en"
    start_firefox(tiktok_url)
  #  xdotool Firefox getwindowgeometry --shell
    ret = a.find(a.i.tiktok_logo, loop=2,timeout=80, timeout_exception="tiktok page didn't open",
                  do_until=del_(start_firefox, [tiktok_url], 30 ))

    if a.find(a.i.login_to_tiktok, loop=1,timeout=5, timeout_exception=None):  raise Exception("tiktok is requesting login")
            
    select_file = a.find(a.i.select_file, loop=2, timeout_exception=True)

    type_hashtags(select_file, "#pop")
    #a.click(select_file.found)  
    a.find(a.i.dict["open_file" + suffix], loop=2,  do_until=del_(a.click, [select_file.found[0:2]], 2 ))
    #a.press("enter")
    a.find(a.i.post, loop=2,  click=1,  do_until=del_(a.press, ["enter"], 2 ))

    a.find(a.i.view_profile, loop=2,  click=1,  timeout=120)
    
    yt_url = f"https://studio.youtube.com/channel/"+yt_id+"/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D" 
    start_firefox(yt_url)
    
    upload_arrow = a.find(a.i.upload_arrow, loop=2,timeout=80, timeout_exception="yt page didn't open",
                    do_until=del_(start_firefox, [yt_url], 30 ))

    a.find(a.i.dict["open_file" + suffix], loop=2,  do_until=del_(a.click, [upload_arrow.found[0:2]], 2 ))

    two_empty = a.find(a.i.two_empty, loop=2,  do_until=del_(a.press, ["center"], 2 ))

    a.type("#pop #shorts")

    a.find(a.i.one_empty, loop=2,   do_until=del_(a.click, [two_empty.found, 0, 13 ], 2 ))

    three_empty = a.find(a.i.three_empty, loop=2,   do_until=del_(a.click, [two_empty.found, 603, 105], 2 ))

    a.find(a.i.one_empty_public, loop=2,   do_until=del_(a.click, [three_empty.found, 0, 45], 2 ))

    a.find(a.i.upload_complete, timeout=120, loop=2)
    
    a.click(two_empty.found,  603,105 )

    a.find(a.i.clipboard, loop=2)

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
    yt_id = network.recv_string(conn)
    a.rlog("Yt id: " + yt_id)
    try:
        browse_task(yt_id)
    except Exception as e:
        a.rlog("Exception: " + traceback.format_exc())
        a.rlog("Exception: " + str(e))


    conn.close()

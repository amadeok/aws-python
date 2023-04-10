import os
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

print(os.getcwd())
print(distro.info())
ubuntu_ver = distro.info()["version"]

home = "amadeok" if ubuntu_ver =="20.04" else "ubuntu"
with open(f"/home/{home}/f.txt",  "w") as ww:
    ww.write(str(datetime.now().strftime("%H:%M:%S")) )
a = at.autopy("images")

prefix = "70p_"


# ret = a.find(a.i.dict[prefix + "select_file"], loop=3)
# if ret:
#     for x in range(2):
#         a.click(ret.found, 140, -232)  
#         time.sleep(0.5)
#     a.type("#pop")
#     time.sleep(1)
#     a.press("enter")

HOST = '188.153.195.184'
PORT = 9596

REM_HOST = "0.0.0.0"
REM_PORT = 4003

# HOST = '192.168.1.230'  # Standard loopback interface address (localhost)
# PORT = 9595


#exit()


if __name__ == '__main__':
    import sys
    port = 9001
    print("lisetining at " + REM_HOST + ":" + str(REM_PORT))

    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
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


    network.recveive_file(os.getcwd() + "/"+  "file.mp4", conn)

    message = "this is a message ç°*Pé*çùà"
    for x in range(10):
        rlog(message + str(x), conn)
        network.send_string(message + str(x), conn)
    conn.close()

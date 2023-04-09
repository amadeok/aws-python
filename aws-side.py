import os
import time
import socket
import atexit
import select
import pyautogui as pg
import autopy as at
import os, platform
from datetime import datetime
import distro

print(os.getcwd())
print(distro.info())
ubuntu_ver = distro.info()["version"]

home = "amadeok" if ubuntu_ver =="20.04" else "ubuntu"
with open(f"/home/{home}/f.txt",  "w") as ww:
    ww.write(str(datetime.now().strftime("%H:%M:%S")) )
a = at.autopy("images")

prefix = "70p_"

ret = False#a.find(a.i.dict[prefix + "select_file"], loop=3)
if ret:
    for x in range(2):
        a.click(ret.found, 140, -232)  
        time.sleep(0.5)
    a.type("#pop")
    time.sleep(1)
    a.press("enter")

HOST = '188.153.195.184'
PORT = 9596

REM_HOST = "0.0.0.0"
REM_PORT = 4003

# HOST = '192.168.1.230'  # Standard loopback interface address (localhost)
# PORT = 9595



#exit()

def recveive_file(save_path, conn):
    b = b"\x00\x00\x00\x01"
    # conn.sendall(b)
    
    size_b = conn.recv(4)
    size = int.from_bytes(size_b, 'little')
    print("receving " + str(size) + " bytes")
    recv_data=[]
    recv_data = b''
    rem = size
    buf = 128000
    f_out = open(save_path, "wb")
    i= 0
    pos =  0
    buffer = bytearray(size)
    while True:
        data=conn.recv(buf)
        buf = len(data)+1
        chunk_size = len(data)
        #c = buffer[pos:chunk_size]
        #print( " c ", len(c), " data ", len(data))
        buffer[pos:pos+chunk_size] = data
        #print(buffer[0:100])
        pos += chunk_size

        i+=1
        if i %200 == 0:
            print(chunk_size)
        rem-= chunk_size
        if (rem < buf):
            buf = rem
        
        #recv_data +=data;
        f_out.write(data)
        #l = len(recv_data)
        if not data or pos >= size:
            break
    
    f_out.close()
        
    #recv_size = len(recv_data)
    if pos != size:
        print("error dif size")

    conn.sendall(buffer) 

    conn.send(b'\x01')
    re = conn.recv(1)
    print(re)

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


    recveive_file(os.getcwd() + "/"+  "file.mp4", conn)
    conn.close()

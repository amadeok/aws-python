import os
import time
import socket
import atexit
import select
HOST = '188.153.195.184'
PORT = 9596

REM_HOST = "localhost"
REM_PORT = 4003

# HOST = '192.168.1.230'  # Standard loopback interface address (localhost)
# PORT = 9595


if __name__ == '__main__':
    import sys
    port = 9001

    while 1:
        try:
            print("lisetining at " + REM_HOST + ":" + str(REM_PORT))
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((REM_HOST, REM_PORT))
                s.listen()
                conn, addr = s.accept()
                print("Socket connected " + addr[0] + ":" + str(addr[1]))
                b = b"\x00\x00\x00\x01"
                # conn.sendall(b)
                
                size_b = conn.recv(4)
                size = int.from_bytes(size_b, 'little')
                print("receving " + str(size) + " bytes")
                recv_data=[]
                recv_data = b''
                rem = size
                buf = 500
                while True:
                  data=conn.recv(buf)
                  rem-= len(data)
                  if (rem < 500):
                    buf = rem
                  l =  0
                # for ch in recv_data:
                    #l += len(ch)
                  recv_data +=data;
                  l = len(recv_data)
                  if not data or l >= size:
                    break
                  
                recv_size = len(recv_data)
                if recv_size != size:
                  print("error dif size")

                conn.sendall(recv_data) 

                re = conn.recv(1)
                print(re)




        except Exception as e:
            print(e)
            time.sleep(1)

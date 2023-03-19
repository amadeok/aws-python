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
                        
                data_cpy = b''
                f = open('I_printed_this.ps', 'wb')
                while True:
                    data = conn.recv(500)
                    data_cpy += data
                    if not data:
                        break
                    f.write(data)
                    f.flush()
                f.close()

                # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # s.connect((HOST, PORT))
                size = len(data_cpy)
                size_bytes = size.to_bytes(4, 'little')
                conn.sendall(size_bytes)
                print("sending all")
                conn.sendall(data_cpy)
                # recv_data = s.recv(size)

                recv_data = b''
                rem = size
                buf = 500
                while True:
                    data = conn.recv(buf)
                    rem -= len(data)
                    if (rem < 500):
                        buf = rem

                    recv_data += data
                    l = len(recv_data)
                    if not data or l >= size:
                        break

                conn.send(b'\x01')

                # recv_data=''.join(recv_data)
                print("recv: " + str(len(recv_data)))
                for n in range(size):
                    if recv_data[n] != data_cpy[n]:
                        print("ERROR tcp tranfer failed " + str(n))

                conn.close()
                time.sleep(0.1)

        except Exception as e:
            print(e)
            time.sleep(1)

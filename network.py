import numpy, time, logging, app_logging, socket,threading, math

def client_connect(port, ip):
    while 1:
        s=  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try:
            logging.info("Connecting to " + ip + ":" + str(port))
            s.connect((ip, port))

            logging.info("Socket connected")
            return s
            break
        
        except Exception as e:
            s.close()

            print(e)
            time.sleep(1)

def server_connect(port, ip):
    print("listening at " + port + ":" + str(port))

    conn =  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    while 1:
        try:
            conn.bind((ip, port))
            conn.listen()
            conn, addr = conn.accept()
            print("Socket connected " + addr[0] + ":" + str(addr[1]))
            break

        except Exception as e:
            print(e)
            time.sleep(1)
            #conn.close()
    return conn

def transfer_task(port, ip, data):
    s = client_connect(port, ip)
    size = len(data)
    size_bytes = size.to_bytes(4, 'little')
    socket.sendall(size_bytes)
    socket.sendall(data)

def receive_task(port, ip, part_n, data_arr):
    conn = server_connect(port, ip)
    size_b = conn.recv(4)
    size = int.from_bytes(size_b, 'little')
    logging.info("receving " + str(size) + " bytes")

    rem = size
    buf = 128000
    i= 0
    pos =  0
    data_arr[part_n] = bytearray(size)
    while True:
        data=conn.recv(buf)
        buf = len(data)+1
        chunk_size = len(data)

        data_arr[part_n][pos:pos+chunk_size] = data
        pos += chunk_size

        rem-= chunk_size
        if (rem < buf):
            buf = rem
        
        if not data or pos >= size:
            break
    if pos != size:
        logging.info("error dif size")
    # conn.sendall(buffer) 

    # conn.send(b'\x01')
    # re = conn.recv(1)
    # logging.info(re)

def file_transfer_mt(file, main_port, parts, ip):
    threads = []
    data_cpy = b''
    with open(file, 'rb') as f:
        data_cpy = f.read()[0:-1]

    part_size = math.ceil(len(data_cpy) / parts)
    tot = 0
    for x in range(parts):
        tot += part_size
    rem = len(data_cpy) - tot
    
    for x in range(parts):
        st = x * part_size
        end = (x+1)*part_size if x < parts-1 else -1
        t = threading.Thread(target=transfer_task, args=(main_port+1+x, ip, data_cpy[st:end]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def recveive_file_mt(save_path, main_port, ip, parts=3):
    data_arr = [None for x in range(parts)]
    threads = []
    for x in range(parts):
        t = threading.Thread(target=receive_task, args=(main_port+1+x, ip, x, data_arr ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    with open(save_path, "wb") as out_:
        for arr in data_arr:
            out_.write(arr)



def file_transfer(file, socket):
    data_cpy = b''
    f = open(file, 'rb')
    data_cpy = f.read()[0:-1]
    f.close()

    #print(data_cpy[0:100])
    # while True:
    #     #data = conn.recv(500)
    #     data_cpy += data
    #     if not data:
    #         break
    #     f.write(data)
    #     f.flush()

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # s.connect((HOST, PORT))
    size = len(data_cpy)
    size_bytes = size.to_bytes(4, 'little')
    socket.sendall(size_bytes)
    #print("sending all")
    socket.sendall(data_cpy)
    # recv_data = s.recv(size)

    recv_data = b''
    rem = size
    buf = 128000
    buffer = bytearray(size)
    pos = 0
    while True:
        data = socket.recv(buf)
        buf = len(data)+1
        chunk_size = len(data)
        buffer[pos:pos+chunk_size] = data

        pos+=chunk_size

        rem -= len(data)
        if (rem < buf):
            buf = rem
        #recv_data += data
       # l = len(recv_data)
        if not data or pos >= size:
            break
        
    # recv_data=''.join(recv_data)
    #print("recv: " + str(pos))
    #buffer[pos-100] = 233
    np_ori = numpy.array(bytearray(data_cpy))
    np_new = numpy.array(buffer)
    eq = numpy.array_equiv(np_new, np_ori)
    assert(eq)
    logging.info(f"transfer success: {eq}")
    # for n in range(size):
    #     if buffer[n] != data_cpy[n]:
    #         print("ERROR tcp tranfer failed " + str(n))

    ret = socket.recv(1)
    i = len(ret)
    logging.info(f"ret {ret}")
    socket.send(b'\x01')

    time.sleep(0.1)


    
def recveive_file(save_path, conn):
    b = b"\x00\x00\x00\x01"
    # conn.sendall(b)
    
    size_b = conn.recv(4)
    size = int.from_bytes(size_b, 'little')
    logging.info("receving " + str(size) + " bytes")
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

       # i+=1
        #if i %200 == 0:
        #    print(chunk_size)
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
        logging.info("error dif size")

    conn.sendall(buffer) 

    conn.send(b'\x01')
    re = conn.recv(1)
    logging.info(re)


def send_string(string, conn):
    mb = bytes(string, 'utf-8')
    size = len(mb)
    size_bytes = size.to_bytes(4, 'little')
    conn.sendall(size_bytes)
    conn.sendall(mb)

def recv_string(conn):
    size_b = conn.recv(4)
    if not size_b:
        return -1
    size = int.from_bytes(size_b, 'little')
    #print("receving " + str(size) + " bytes")
    data=conn.recv(size)
    return data.decode("utf-8")
    print(str(data))



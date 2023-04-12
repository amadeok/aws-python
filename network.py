import numpy, time

def file_transfer(file, socket):
    data_cpy = b''
    f = open(file, 'rb')
    data_cpy = f.read()[0:-1]
    #print(data_cpy[0:100])
    # while True:
    #     #data = conn.recv(500)
    #     data_cpy += data
    #     if not data:
    #         break
    #     f.write(data)
    #     f.flush()
    f.close()

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # s.connect((HOST, PORT))
    size = len(data_cpy)
    size_bytes = size.to_bytes(4, 'little')
    socket.sendall(size_bytes)
    print("sending all")
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
    print("recv: " + str(pos))
    #buffer[pos-100] = 233
    np_ori = numpy.array(bytearray(data_cpy))
    np_new = numpy.array(buffer)
    eq = numpy.array_equiv(np_new, np_ori)
    assert(eq)
    print("transfer success: ", eq)
    # for n in range(size):
    #     if buffer[n] != data_cpy[n]:
    #         print("ERROR tcp tranfer failed " + str(n))

    ret = socket.recv(1)
    i = len(ret)
    print("ret", str(ret))
    socket.send(b'\x01')

    time.sleep(0.1)


    
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
        print("error dif size")

    conn.sendall(buffer) 

    conn.send(b'\x01')
    re = conn.recv(1)
    print(re)


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



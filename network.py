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
    np_ori = numpy.array(bytearray(data_cpy))
    np_new = numpy.array(buffer)
    print("transfer success: ", numpy.array_equiv(np_new, np_ori))
    # for n in range(size):
    #     if buffer[n] != data_cpy[n]:
    #         print("ERROR tcp tranfer failed " + str(n))

    ret = socket.recv(1)
    i = len(ret)
    print("ret", str(ret))
    socket.send(b'\x01')

    time.sleep(0.1)
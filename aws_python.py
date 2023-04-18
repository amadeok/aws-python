#Python Program for creating a connection
import boto3
import numpy
import logging, network, os
import app_logging
import boto3_utils as b3
import socket
from subprocess import Popen, PIPE, STDOUT
import time, random
import sqlite3 as sl
import sql_utils

class aws_handler():
    def __init__(s) -> None:

        if os.path.isfile("rtf"):
            with open("rtf", "r")as i:
                d = i.read().splitlines()
                s.access_key_id = d[0]
                s.secret_access_key = d[1]
        else:
            raise Exception("Missing aws keys")

        s.debug_mode = 0
        s.client = None
        s.sql = sql_utils.sql_()
        s.local = 0
        s.start_vnc = 1

    def aws_task(s, inst_name, ctx, stop_instance, hashtags,  inst_id = None, yt_ch_id=None):
        logging.info(f"Starting aws task instance {inst_name}")

        aws_id, yt_id, region, mail, name  = s.sql.get_row(inst_name)
        s.sql.add_update_table_col(name)
        s.sql.add_track(ctx.input_f.win_name)
        if inst_id: aws_id = inst_id
        if yt_ch_id: yt_id = yt_ch_id

        s.client = boto3.client('ec2', region, aws_access_key_id=s.access_key_id, aws_secret_access_key=s.secret_access_key)

        InstanceIds=[ aws_id ]
        YtChannelIds= [yt_id ]  ##"UCRFWvTVdgkejtxqh0jSlXBg" amadeokusch ############ ###UC09k3A2-21bxqFaYb6gdK0w === musicosmus   ## "UCg_-P7-Kkmgg7ehNzV2jQZQ"  = amadeokusch2    ##'UCLnYo095mUIHYQikbsueFdw' === theristhere    ]

        if not s.local:
            try:
                rest = s.client.start_instances( InstanceIds=InstanceIds)
            except Exception as e:
                logging.info(e)
            ret = [[]]
            while len(ret[0]) == 0:
                ret = b3.gather_public_ip(region, s.client)

        tt = time.time()

        instance_ip = ret[0][0][0] if not s.local else  "192.168.1.160"#79.42.227.212" # "192.168.1.160" #"127.0.0.1"
        if not s.local and s.start_vnc:
            p = Popen([r"C:\Program Files\RealVNC\VNC Viewer\vncviewer.exe", f'{instance_ip}:1'])

        logging.info(f"Instance ip: {instance_ip} ")
        REM_HOST = instance_ip #'192.168.1.189'  # Standard loopback interface address (localhost)
        REM_PORT = 4003    # Port to listen on (non-privileged ports are > 1023)
    
        # fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\00002(5)\tmp\\"
        # file_ = fld + random.choice(os.listdir(fld))
        # file_ = r"C:\Users\amade\Documents\dawd\Exported\00030 like you promised\00030.mov"
        #file_ =  r"D:\videos\VID_20200529_192704.mp4"
        file_ = ctx.input_f.dav_final_file

        conn = network.client_connect(REM_PORT, REM_HOST)

        mt = True
        network.send_string("1" if mt else "0", conn)
        parts = 3

        if mt:
            network.send_string(f"{parts}", conn)
            network.file_transfer_mt(file_, REM_PORT, parts, REM_HOST)
        else:
            network.file_transfer(file_, conn)

        #logging.info(f"transfer size {os.stat(file_).st_size} took {(time.time()  - t_)/60:<3} mins")
        network.send_string(YtChannelIds[0] if YtChannelIds[0] else "" , conn)
        network.send_string(hashtags, conn)

        while 1:
            str = network.recv_string(conn)
            if str == -1:
                print("connection closed")
                break
            elif str == "TT_SUCCESS":
                s.sql.set_record(name, ctx.input_f.win_name, 1, "TT_Uploads")
                logging.info(str)
            elif str == "YT_SUCCESS":
                s.sql.set_record(name, ctx.input_f.win_name, 1, "YT_Uploads")
                logging.info(str)
            else:
                print(str)

        logging.info(f"aws task took aprox : {tt - time.time()}")
        if stop_instance:
            logging.info(f"stopping instance..")
            rest = s.client.stop_instances( InstanceIds=InstanceIds)

        

#rest = client.reboot_instances( InstanceIds=InstanceIds) 
# ret = b3.gather_public_ip()
# print(get_instance_state(client, InstanceIds[0]))
# try:
#resp = client.stop_instances( InstanceIds=InstanceIds)
# except Exception as e:
#     logging.info(f"failed to stop instance {e}")
# print(get_instance_state(client, InstanceIds[0]))
# try:
# except Exception as e:
#     logging.info(f"failed to start instance {e}")

# state = get_instance_state(client, InstanceIds[0])

# if state != "running":
#      rest = client.start_instances( InstanceIds=InstanceIds)
#resp = client.stop_instances( InstanceIds=InstanceIds)

#print(response)

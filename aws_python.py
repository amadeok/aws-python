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
from datetime import datetime

def get_tt_and_ty_do(sql, ctx, name, row, do_tt=True, do_yt=True):
    aws_id, yt_id, region,  name, tt_mail, yt_mail , ch_name, do_tt, do_yt, add_text = row
    tt = sql.get_record(name, ctx.input_f.win_name, "TT_Uploads")
    do_tt = tt != "1" and do_tt and (len(tt_mail) if tt_mail else False) or do_tt == "f"
    yt = sql.get_record(name, ctx.input_f.win_name, "YT_Uploads")
    do_yt = yt != "1" and do_yt and (len(yt_mail) if yt_mail else False) or do_yt == "f"
    return do_tt, do_yt


class aws_handler():
    def __init__(s, sql=None) -> None:

        if os.path.isfile("rtf"):
            with open("rtf", "r")as i:
                d = i.read().splitlines()
                s.access_key_id = d[0]
                s.secret_access_key = d[1]
        else:
            raise Exception("Missing aws keys")

        s.debug_mode = 0
        s.client = None
        s.sql = sql_utils.sql_() if not sql else sql
        s.local = 0
        s.start_vnc = 0


    def parse_task(s, tt_mail, parsed, text0, text1, suffix=""):
        try:
            nn = suffix + "_" + tt_mail.split(r"@")[0]
            parsed_s =  parsed.split(text0)
            parsed_p = parsed_s[1]
            parsed_s2 =  parsed_p.split(text1)
            parsed_p2 = parsed_s2[0]

            with open(f"vis/{nn}.txt", "a",  encoding="utf-8") as fff:
                fff.write("\n### New entry " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n" + parsed_p2) 

        except Exception as e:
            logging.info("Failed to process parsed text")
            with open(f"vis/{nn}.txt", "a",  encoding="utf-8") as fff:
                fff.write("\n###New entry " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n" + parsed) 

    def delete_files(s, ctx):
        sql_utils.delete_file(ctx.input_f.avee_final_file)
        #sql_utils.delete_file(ctx.input_f.dav_final_file)
        sql_utils.delelte_files_in_folder(ctx.input_f.out_fld + "\\tmp\\")





    def aws_task(s, ctx,  hashtags,  inst_id = None, yt_ch_id=None, do_tt=True, do_yt=True):

        reboot_inst=ctx.reboot_inst
        stop_instance=ctx.stop_inst

        inst_name = ctx.instance_name
        row = s.sql.get_row(inst_name)
        aws_id, yt_id, region,  name, tt_mail, yt_mail , ch_name, do_tt, do_yt, add_text = row

        do_tt, do_yt = get_tt_and_ty_do(s.sql,ctx, inst_name, row)
        if not do_tt and not do_yt or '!' in row[3]:
            logging.info("No TT or YT task to perform, returning")
            return      

        logging.info(f"Starting aws task instance {inst_name}")

        time_start = time.time()

        if not s.local:
            s.sql.add_update_table_col(name)
        if name == None or name == "None":
            logging.info("Name is none")
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

            if reboot_inst:
                s.client.reboot_instances( InstanceIds=InstanceIds)
            ret = [[]]
            while len(ret[0]) == 0:
                time.sleep(1)
                try:
                    ret = b3.gather_public_ip(region, s.client)
                except Exception as e:
                    logging.info(e)


        instance_ip = ret[0][0][0] if not s.local else  "192.168.1.160"#79.42.227.212" # "192.168.1.160" #"127.0.0.1"
        if not s.local and s.start_vnc:
            p = Popen([r"C:\Program Files\RealVNC\VNC Viewer\vncviewer.exe", f'{instance_ip}:1'])

        logging.info(f"Instance ip: {instance_ip} ")
        REM_HOST = instance_ip #'192.168.1.189'  # Standard loopback interface address (localhost)
        REM_PORT = 4003    # Port to listen on (non-privileged ports are > 1023)
    
        # fld = f"{app_env.ld_shared_folder}\output\00002(5)\tmp\\"
        # file_ = fld + random.choice(os.listdir(fld))
        # file_ = r"C:\Users\amade\Documents\dawd\Exported\00030 like you promised\00030.mov"
        #file_ =  r"D:\videos\VID_20200529_192704.mp4"
        file_ = ctx.input_f.dav_final_file

        conn = network.client_connect(REM_PORT, REM_HOST)
        network.send_string("1" if do_tt else "0", conn)
        network.send_string("1" if do_yt else "0", conn)

        remote_sha = network.recv_string(conn)
        if (remote_sha == app_logging.sha):
            logging.info(f"repos match: {remote_sha}")
        else:
            raise Exception(f"Repos don't match local: {app_logging.sha} remote: {remote_sha}")

        mt = True
        network.send_string("1" if mt else "0", conn)
        parts = 1

        if mt:
            network.send_string(f"{parts}", conn)
            network.file_transfer_mt(file_, REM_PORT, parts, REM_HOST)
        else:
            network.file_transfer(file_, conn)

        #logging.info(f"transfer size {os.stat(file_).st_size} took {(time.time()  - t_)/60:<3} mins")
        network.send_string(YtChannelIds[0] if YtChannelIds[0] else "" , conn)
        network.send_string(hashtags, conn)

        tt_parsed = ""
        yt_parsed = ""
        while 1:
            str = network.recv_string(conn)
            if str == -1:
                print("connection closed")
                break
            elif str == "TT_SUCCESS":
                if not s.local:
                    s.sql.set_record(name, ctx.input_f.win_name, 1, "TT_Uploads")
                logging.info(str)
            elif str == "YT_SUCCESS":
                if not s.local:
                    s.sql.set_record(name, ctx.input_f.win_name, 1, "YT_Uploads")
                logging.info(str)
            elif str == "TT_PARSE":
                tt_parsed = network.recv_string(conn)        
            elif str == "YT_PARSE":
                yt_parsed = network.recv_string(conn)          
            else:
                print(str)
        
        if tt_mail and len(tt_mail) and yt_mail and len(yt_mail):
            tt = s.sql.get_record(name, ctx.input_f.win_name, "TT_Uploads")
            yt = s.sql.get_record(name, ctx.input_f.win_name, "YT_Uploads")
            if tt == "1" and yt  == "1":
                s.delete_files(ctx)
        elif tt_mail and len(tt_mail) and s.sql.get_record(name, ctx.input_f.win_name, "TT_Uploads") == "1":
            s.delete_files(ctx)        
        elif yt_mail and len(yt_mail) and s.sql.get_record(name, ctx.input_f.win_name, "YT_Uploads") == "1":
            s.delete_files(ctx)

        sql_utils.delete_file(ctx.input_f.avee_final_file)
        sql_utils.delelte_files_in_folder(ctx.input_f.out_fld + "\\tmp\\")

        if len(tt_parsed):
            s.parse_task(tt_mail, tt_parsed, "Videos\n\nLiked\n", "Get app\nGet TikTok App\n", "tt")
        if len(yt_parsed):
            s.parse_task(yt_mail, yt_parsed,  "Likes (vs. dislikes)" , "Rows per page:", "yt")
            

        logging.info(f"aws task took aprox : {time.time() -time_start } secs")
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

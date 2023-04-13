#Python Program for creating a connection
import boto3
import numpy
import logging, network, os
import app_logging
import boto3_utils as b3
import socket
from subprocess import Popen, PIPE, STDOUT
import time, random

access_key_id = "AKIAQTONZDFNOK7WKRXN"
secret_access_key = "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"

if os.path.isfile("rtf"):
    with open("rtf", "r")as i:
        d = i.read().splitlines()
        access_key_id = d[0]
        secret_access_key = d[1]

region = "ap-southeast-4" #'ap-south-1'
ec2 = boto3.client('ec2',
                   region,
                   aws_access_key_id=access_key_id,
                   aws_secret_access_key=secret_access_key)
    
if __name__ == '__main__':
    ec2_res = boto3.resource('ec2',
                   region,
                   aws_access_key_id=access_key_id,
                   aws_secret_access_key=secret_access_key)
    #hello_ec2(ec2_res)
    client = boto3.client('ec2',
                   region,
                   aws_access_key_id=access_key_id,
                   aws_secret_access_key=secret_access_key)

    InstanceIds=[        'i-0f7cb6f8639cff05c',    ]
    YtChannelIds=[        'UCLnYo095mUIHYQikbsueFdw',    ]


local = True

#rest = client.reboot_instances( InstanceIds=InstanceIds) 
# ret = b3.gather_public_ip()
# print(get_instance_state(client, InstanceIds[0]))
# try:
#resp = client.stop_instances( InstanceIds=InstanceIds)
# except Exception as e:
#     logging.info(f"failed to stop instance {e}")
# print(get_instance_state(client, InstanceIds[0]))
# try:
if 0:
    #rest = client.start_instances( InstanceIds=InstanceIds)
    ret = [[]]
    while len(ret[0]) == 0:
        ret = b3.gather_public_ip()
# except Exception as e:
#     logging.info(f"failed to start instance {e}")

# state = get_instance_state(client, InstanceIds[0])

# if state != "running":
#      rest = client.start_instances( InstanceIds=InstanceIds)
#resp = client.stop_instances( InstanceIds=InstanceIds)

#print(response)

instance_ip = ret[0][0][0] if not local else  "192.168.1.160"#79.42.227.212" # "192.168.1.160" #"127.0.0.1"
logging.info(f"Instance ip: {instance_ip} ")
REM_HOST = instance_ip #'192.168.1.189'  # Standard loopback interface address (localhost)
REM_PORT = 4003    # Port to listen on (non-privileged ports are > 1023)
print_ps_directly = True
fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\00002(5)\tmp\\"
file_ = fld + random.choice(os.listdir(fld))
file_ = r"C:\Users\amade\Documents\dawd\Exported\00030 like you promised\00030.mov"


while 1:
    s=  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    try:
        logging.info("Connecting to " + REM_HOST + ":" + str(REM_PORT))
        s.connect((REM_HOST, REM_PORT))

        logging.info("Socket connected")
        break
    
    except Exception as e:
        s.close()

        print(e)
        time.sleep(1)

network.file_transfer(file_, s)
network.send_string(YtChannelIds[0], s)
network.send_string("#pop", s)

while 1:
    str = network.recv_string(s)
    if str == -1:
        print("connection closed")
        break
    else:
        print(str)


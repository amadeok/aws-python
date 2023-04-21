from sql_utils import sql_
import logging
import git, os, random
import argparse, distro
from subprocess import Popen
import boto3, boto3_utils as b3

parser = argparse.ArgumentParser()
parser.add_argument("--iname", help="instance name", default=False)
parser.add_argument("--log_level", help="log level", default=logging.DEBUG )

args = parser.parse_args()


if os.path.isfile("rtf"):
    with open("rtf", "r")as i:
        d = i.read().splitlines()
        access_key_id = d[0]
        secret_access_key = d[1]
else:
    raise Exception("Missing aws keys")

sql = sql_()
aws_id, yt_id, region,  name, tt_mail, yt_mail, ch_name  = sql.get_row(args.iname)

client = boto3.client('ec2', region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

InstanceIds=[ aws_id ]
YtChannelIds= [yt_id ] 

if 1:
    # try:
    #     rest = client.start_instances( InstanceIds=InstanceIds)
    # except Exception as e:
    #     logging.info(e)

    #if reboot_inst:
    #    client.reboot_instances( InstanceIds=InstanceIds)
    ret = [[]]
    while len(ret[0]) == 0:
        ret = b3.gather_public_ip(region, client)


instance_ip = ret[0][0][0] 

p = Popen([r"C:\Program Files\RealVNC\VNC Viewer\vncviewer.exe", f'{instance_ip}:1'])
p.wait()


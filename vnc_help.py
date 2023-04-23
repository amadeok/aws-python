from sql_utils import sql_
import logging
import git, os, random
import argparse, distro
from subprocess import Popen
import boto3, boto3_utils as b3

parser = argparse.ArgumentParser()
parser.add_argument("-n", help="instance name", default="")
parser.add_argument("-s", help="ssh", type=str, default=False )
parser.add_argument("-q", help="stop instance", type=bool, default=False )
parser.add_argument("-r", help="reboot instance", type=bool, default=False )

args = parser.parse_args()


if os.path.isfile("rtf"):
    with open("rtf", "r")as i:
        d = i.read().splitlines()
        access_key_id = d[0]
        secret_access_key = d[1]
else:
    raise Exception("Missing aws keys")

sql = sql_()


if args.n == "check":
    
    pass
    for row in sql.cur.execute('''SELECT * FROM Main '''):
        
        logging.info(row)

        ec2 = boto3.client('ec2', region_name=row[2],  aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
        instance_id =row[0]

        response = ec2.describe_instances(InstanceIds=[instance_id])

        state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if state == 'running':
            print(f'! ! ! The EC2 instance {row[2]} {row[3]} is running')
        else:
            print(f'The EC2 instance {row[2]} {row[3]}  is in {state} state')
    input()

else:
    aws_id, yt_id, region,  name, tt_mail, yt_mail, ch_name  = sql.get_row(args.n)

    client = boto3.client('ec2', region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    InstanceIds=[ aws_id ]
    YtChannelIds= [yt_id ] 

    if args.q:
        rest = client.stop_instances( InstanceIds=InstanceIds)
        exit()
    if args.r:
        rest = client.reboot_instances( InstanceIds=InstanceIds)
        exit()
    if 1:
        try:
            rest = client.start_instances( InstanceIds=InstanceIds)
        except Exception as e:
            logging.info(e)

        #if reboot_inst:
        #    client.reboot_instances( InstanceIds=InstanceIds)
        ret = [[]]
        while len(ret[0]) == 0:
            ret = b3.gather_public_ip(region, client)

    import os

    instance_ip = ret[0][0][0] 
    if args.s == "True" or args.s == "true"or args.s == "1" or args.s == True:

        ipp = instance_ip.replace(".", "-")
        pem = f"C:\\Users\\amade\\{region}.pem" if os.name == 'nt' else f"/home/amadeok/{region}.pem"

        command = f'ssh -i "{pem}" ubuntu@ec2-{ipp}.{region}.compute.amazonaws.com'
        #p = Popen(["start", "ssh", "-i", f"C:\\Users\\amade\\{region}.pem", f"ubuntu@ec2-{ipp}.{region}.compute.amazonaws.com"])

        os.system(command)
        print()
    else:
        p = Popen([r"C:\Program Files\RealVNC\VNC Viewer\vncviewer.exe", f'{instance_ip}:1', "-KeepAliveResponseTimeout", "60"])
        p.wait()

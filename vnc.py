from sql_utils import sql_
import logging, time
import git, os, random
import argparse, distro, threading
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


if "check" in args.n:
    rows = []
    if args.n != "check":
        ss = args.n.split(":")
        ss = ss[1:len(ss)]
        for elem in ss:
            rows.append(sql.get_row(elem))
    else:
        for i, row in enumerate(sql.cur.execute('''SELECT * FROM Main ''')):
            rows.append(row)
    
    def get_instance_state(row, region, instance_id, name):
        #region, instance_id =  row[2], row[0]
        logging.info(row)

        ec2 = boto3.client('ec2', region_name=region,  aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

        response = ec2.describe_instances(InstanceIds=[instance_id])

        state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if state == 'running':
            print(f'! ! ! The EC2 instance {row[0]:<2} {name:<10}  {region:<20} is running')
        else:
            print(f'The EC2 instance {row[0]:<2} {name:<10}  {region:<20}   is in {state} state')
    ts = []
    for i, row in enumerate(rows):
        t = threading.Thread(target=get_instance_state, args=([i, row], row[2], row[0], row[3]))
        ts.append(t)
        t.start()
        time.sleep(0.01)

    for tt in ts:
        tt.join()
        

        #get_instance_state(row, row[2], row[0], row[3])
    print("Press enter to exit")
    input()

else:
    aws_id, yt_id, region,  name, tt_mail, yt_mail, ch_name, dott, doyt, addtext = sql.get_row(args.n)

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
        if "us-east-1" in region:
            command = f'ssh -i "{pem}" ubuntu@ec2-{ipp}.compute-1.amazonaws.com'
        else:
            command = f'ssh -i "{pem}" ubuntu@ec2-{ipp}.{region}.compute.amazonaws.com'
        #p = Popen(["start", "ssh", "-i", f"C:\\Users\\amade\\{region}.pem", f"ubuntu@ec2-{ipp}.{region}.compute.amazonaws.com"])

        os.system(command)
        print()
    else:
        p = Popen([r"C:\Program Files\RealVNC\VNC Viewer\vncviewer.exe", f'{instance_ip}:1', "-KeepAliveResponseTimeout", "180"])
        p.wait()

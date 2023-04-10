#Python Program for creating a connection
import boto3
import numpy
import logging, network
import app_logging

access_key_id = "AKIAQTONZDFNOK7WKRXN"
secret_access_key = "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"

with open("rtf", "r")as i:
    d = i.read().splitlines()
    access_key_id = d[0]
    secret_access_key = d[1]

region = "ap-southeast-4" #'ap-south-1'
ec2 = boto3.client('ec2',
                   region,
                   aws_access_key_id=access_key_id,
                   aws_secret_access_key=secret_access_key)
 
#This function will describe all the instances
#with their current state
#response = ec2.describe_instances()

def hello_ec2(ec2_resource):

    for sg in ec2_resource.security_groups.limit(10):
        print(f"\t{sg.id}: {sg.group_name}")



class InstanceWrapper2:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions."""
    def __init__(self, ec2_resource, instance=None):
        self.ec2_resource = ec2_resource
        self.instance = instance

    @classmethod
    def from_resource(cls):
        ec2_resource = boto3.resource('ec2')
        return cls(ec2_resource)

    def start(self):
        if self.instance is None:
            print("No instance to start.")
            return

        try:
            response = self.instance.start()
            self.instance.wait_until_running()
        except Exception as err:
            print(
                "Couldn't start instance %s. Here's why: %s: %s", self.instance.id,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response
        

class InstanceWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions."""
    def __init__(self, ec2_resource, instance=None):

        self.ec2_resource = ec2_resource
        self.instance = instance

    @classmethod
    def from_resource(cls):
        ec2_resource = boto3.resource('ec2')
        return cls(ec2_resource)

    def display(self, indent=1):

        if self.instance is None:
            print("No instance to display.")
            return

        try:
            self.instance.load()
            ind = '\t'*indent
            print(f"{ind}ID: {self.instance.id}")
            print(f"{ind}Image ID: {self.instance.image_id}")
            print(f"{ind}Instance type: {self.instance.instance_type}")
            print(f"{ind}Key name: {self.instance.key_name}")
            print(f"{ind}VPC ID: {self.instance.vpc_id}")
            print(f"{ind}Public IP: {self.instance.public_ip_address}")
            print(f"{ind}State: {self.instance.state['Name']}")
        except Exception as err:
            print(
                "Couldn't display your instance. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise



# from autopyBot import autopy
# p = r"F:\all\GitHub\Med2000bot\imgs"
# a = autopy.autopy(p)
# ret = a.find(a.i.No, loop=1)
# exit()

def get_instance_state(client, id):
    response = client.describe_instance_status(InstanceIds=[id])
    try:
        return response['InstanceStatuses'][0]['InstanceState']["Name"]
    except Exception as e:
        logging.info(e)
        return "None"
    
        
def gather_public_ip():
    global region
    regions = [region]
    combined_list = []   ##This needs to be returned
    for region in regions:
        instance_information = [] # I assume this is a list, not dict
        ip_dict = {}
        client = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                              region_name=region, )
        descr = client.describe_instances()
        instance_dict = descr.get('Reservations')
        for reservation in instance_dict:
            for instance in reservation['Instances']: # This is rather not obvious
               if instance['State']['Name'] == 'running' and instance['PublicIpAddress'] != None:
                    ipaddress = instance['PublicIpAddress']
                    tagValue = instance['Tags'][0]['Value'] # 'Tags' is a list, took the first element, you might wanna switch this
                    zone = instance['Placement']['AvailabilityZone']
                    info = ipaddress, tagValue, zone, instance["InstanceId"]
                    instance_information.append(info)
        combined_list.append(instance_information)
    return combined_list
        
    
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

    #ret = gather_public_ip()


    # rest = client.reboot_instances( InstanceIds=InstanceIds) 



    # print(get_instance_state(client, InstanceIds[0]))
    # try:
    #resp = client.stop_instances( InstanceIds=InstanceIds)
    # except Exception as e:
    #     logging.info(f"failed to stop instance {e}")

    # print(get_instance_state(client, InstanceIds[0]))
    # try:
    if 0:
        rest = client.start_instances( InstanceIds=InstanceIds)
    ret = [[]]
    while len(ret[0]) == 0:
        ret = gather_public_ip()

    # except Exception as e:
    #     logging.info(f"failed to start instance {e}")

    # state = get_instance_state(client, InstanceIds[0])



    # "running"
    
   # if state != "running":
  #      rest = client.start_instances( InstanceIds=InstanceIds)
    #resp = client.stop_instances( InstanceIds=InstanceIds)

    # i = InstanceWrapper(ec2_resource=ec2_res)
    # i.display()
    # print(i)

#print(response)
import socket, time
local = False
from subprocess import Popen, PIPE, STDOUT
instance_ip = ret[0][0][0] if not local else  "192.168.1.160" #"127.0.0.1"
logging.info(f"Instance ip: {instance_ip} ")
REM_HOST = instance_ip #'192.168.1.189'  # Standard loopback interface address (localhost)
REM_PORT = 4003     # Port to listen on (non-privileged ports are > 1023)
print ("started")
import time, random, os
print_ps_directly = True
fld = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\00002(5)\tmp\\"
file_ = fld + random.choice(os.listdir(fld))
#file_ = r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\00002(5).mp3"


while 1:
    s=  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    try:
        print("Connecting to " + REM_HOST + ":" + str(REM_PORT))
        s.connect((REM_HOST, REM_PORT))

        print("Socket connected")
        break
    
    except Exception as e:
        s.close()

        print(e)
        time.sleep(1)

network.file_transfer(file_, s)
while 1:
    str = network.recv_string(s)
    if str == -1:
        print("connection closed")
        break
    else:
        print(str)


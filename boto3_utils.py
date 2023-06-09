#Python Program for creating a connection
import boto3
import numpy
import logging,  os

access_key_id = "AKIAQTONZDFNOK7WKRXN"
secret_access_key = "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"


if os.path.isfile("rtf"):
    with open("rtf", "r")as i:
        d = i.read().splitlines()
        access_key_id = d[0]
        secret_access_key = d[1]

#region = "ap-southeast-4" #'ap-south-1'
# ec2 = boto3.client('ec2',
#                    region,
#                    aws_access_key_id=access_key_id,
#                    aws_secret_access_key=secret_access_key)
 
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


def get_instance_state(client, id):
    response = client.describe_instance_status(InstanceIds=[id])
    try:
        return response['InstanceStatuses'][0]['InstanceState']["Name"]
    except Exception as e:
        logging.info(e)
        return "None"
    
        
def gather_public_ip(region, client):
    regions = [region] #us-east-1a	should be us-east-1
    combined_list = []   ##This needs to be returned
    for region in regions:
        instance_information = [] # I assume this is a list, not dict
        ip_dict = {}
        #client = boto3.client('ec2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
        #                      region_name=region, )
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
    
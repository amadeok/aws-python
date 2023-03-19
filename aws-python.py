#Python Program for creating a connection
import boto3

access_key_id = "AKIAQTONZDFNOK7WKRXN"
secret_access_key = "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"
region = "ap-southeast-4" #'ap-south-1'
ec2 = boto3.client('ec2',
                   region,
                   aws_access_key_id=access_key_id,
                   aws_secret_access_key=secret_access_key)
 
#This function will describe all the instances
#with their current state
#response = ec2.describe_instances()

def hello_ec2(ec2_resource):
    """
    Use the AWS SDK for Python (Boto3) to create an Amazon Elastic Compute Cloud
    (Amazon EC2) resource and list the security groups in your account.
    This example uses the default settings specified in your shared credentials
    and config files.

    :param ec2_resource: A Boto3 EC2 ServiceResource object. This object is a high-level
                         resource that wraps the low-level EC2 service API.
    """
    print("Hello, Amazon EC2! Let's list up to 10 of your security groups:")
    for sg in ec2_resource.security_groups.limit(10):
        print(f"\t{sg.id}: {sg.group_name}")



class InstanceWrapper2:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions."""
    def __init__(self, ec2_resource, instance=None):
        """
        :param ec2_resource: A Boto3 Amazon EC2 resource. This high-level resource
                             is used to create additional high-level objects
                             that wrap low-level Amazon EC2 service actions.
        :param instance: A Boto3 Instance object. This is a high-level object that
                           wraps instance actions.
        """
        self.ec2_resource = ec2_resource
        self.instance = instance

    @classmethod
    def from_resource(cls):
        ec2_resource = boto3.resource('ec2')
        return cls(ec2_resource)

    def start(self):
        """
        Starts an instance and waits for it to be in a running state.

        :return: The response to the start request.
        """
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
        """
        :param ec2_resource: A Boto3 Amazon EC2 resource. This high-level resource
                             is used to create additional high-level objects
                             that wrap low-level Amazon EC2 service actions.
        :param instance: A Boto3 Instance object. This is a high-level object that
                           wraps instance actions.
        """
        self.ec2_resource = ec2_resource
        self.instance = instance

    @classmethod
    def from_resource(cls):
        ec2_resource = boto3.resource('ec2')
        return cls(ec2_resource)

    def display(self, indent=1):
        """
        Displays information about an instance.

        :param indent: The visual indent to apply to the output.
        """
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
# a.find(a.i.No, loop=1)

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
    #rest = client.reboot_instances( InstanceIds=InstanceIds)

#    rest = client.start_instances( InstanceIds=InstanceIds)
    #resp = client.stop_instances( InstanceIds=InstanceIds)

    # i = InstanceWrapper(ec2_resource=ec2_res)
    # i.display()
    # print(i)

#print(response)
import socket, time

from subprocess import Popen, PIPE, STDOUT

REM_HOST = '16.50.43.4'  # Standard loopback interface address (localhost)
REM_PORT = 4003     # Port to listen on (non-privileged ports are > 1023)
print ("started")
import time
print_ps_directly = True
while 1:
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          print("Connecting to " + REM_HOST + ":" + str(REM_PORT))
          s.connect((REM_HOST, REM_PORT))
          conn, addr = s.accept()

          print("Socket connected")
          while 1:
              

              
                data_cpy = b''
                f = open('I_printed_this.ps', 'wb')
                while True:
                    data = conn.recv(500)
                    data_cpy += data
                    if not data:
                        break
                    f.write(data)
                    f.flush()
                f.close()

                # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # s.connect((HOST, PORT))
                size = len(data_cpy)
                size_bytes = size.to_bytes(4, 'little')
                conn.sendall(size_bytes)
                print("sending all")
                conn.sendall(data_cpy)
                # recv_data = s.recv(size)

                recv_data = b''
                rem = size
                buf = 500
                while True:
                    data = conn.recv(buf)
                    rem -= len(data)
                    if (rem < 500):
                        buf = rem

                    recv_data += data
                    l = len(recv_data)
                    if not data or l >= size:
                        break

                conn.send(b'\x01')

                # recv_data=''.join(recv_data)
                print("recv: " + str(len(recv_data)))
                for n in range(size):
                    if recv_data[n] != data_cpy[n]:
                        print("ERROR tcp tranfer failed " + str(n))

                conn.close()
                time.sleep(0.1)
                # f=open('I_recved_this.Ps','wb')

                # f.write(recv_data)
                # f.flush()
                # f.close()
                
                # if print_ps_directly:
                #   print("running :"  + str(ps_print))
                #   p = Popen(ps_print, stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
                #   grep_stdout = p.communicate(input=recv_data)[0]

                # else:
                #   p = Popen(gs_ps_pdf, stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
                #   grep_stdout = p.communicate(input=recv_data)[0]

                  # f=open('converted.pdf','wb')
                  # f.write(grep_stdout)
                  # f.flush()

                #   p.wait()
                #   print("to pdf")
                #   grep_stdout = grep_stdout[37:-1]

                #   p = Popen(print_cmd,  stdout=PIPE, stdin=PIPE, stderr=STDOUT)      
                #   grep_stdout2 = p.communicate(input=grep_stdout)[0]
                #   print(grep_stdout2)
                #   p.wait()
    except Exception as e:
      print(e)
      time.sleep(1)
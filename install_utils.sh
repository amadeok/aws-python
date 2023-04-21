#!/bin/bash

sudo apt-get update  -y
echo "installing mate.."
#sudo apt-get install x2goserver x2goserver-xsession -y
sudo apt install tasksel  -y
sudo tasksel install ubuntu-mate-desktop
echo "installing tigervnc.."

#sudo apt-get install tightvncserver  -y
sudo apt install tigervnc-standalone-server -y

echo "setting up tigervnc service.."

sudo touch /etc/systemd/system/tigervnc@1.service
sudo cat /etc/systemd/system/tigervnc@1.service

string="[Unit]\nDescription=Remote desktop service (VNC)\nAfter=syslog.target network.target\n\n[Service]\nType=simple\nUser=ubuntu\nPAMName=ubuntu\nPIDFile=/home/ubuntu/.vnc/%H%i.pid\nExecStart=/usr/bin/vncserver -localhost no :1\nExecStop=/usr/bin/vncserver -kill %i\n\n[Install]\nWantedBy=multi-user.target"

echo  -e "$string"  | sudo tee /etc/systemd/system/tigervnc@1.service

sudo systemctl enable tigervnc@1.service
sudo systemctl daemon-reload
sudo systemctl enable tigervnc@1
vncserver -kill :1
sudo systemctl start tigervnc@1.service
sudo systemctl  status tigervnc@1.service

echo "installing xdotool.."

sudo apt install xdotool  -y

echo "install python3.8 and modules.."
sudo apt install python3.8 -y

sudo apt install python3-pip  xclip -y
python3.8 -m pip install -U --force-reinstall pip
python3.8 -m pip install mss pyautogui serial opencv-python keyboard pyKey distro random-word git-python
sudo apt-get install python3-tk python3-dev  -y
#sudo apt-get install pypy-dev

echo "setting up aws python service.."

sudo cat /etc/systemd/system/pythonfile.service

echo  -e '[Unit]\nDescription=python_aws\nAfter=multi-user.target\n\n[Service]\nType=simple\nUser=ubuntu\nEnvironment="DISPLAY=:1"\nWorkingDirectory=/home/ubuntu/aws-python/\nExecStart=/usr/bin/python3.8 /home/ubuntu/aws-python/aws-side.py\nExecStartPre=/usr/bin/git -C /home/ubuntu/aws-python/ pull\n\n[Install]\nWantedBy=multi-user.target'  | sudo tee /etc/systemd/system/pythonfile.service

sudo systemctl daemon-reload && sudo systemctl enable pythonfile.service && sudo systemctl start pythonfile.service && sudo systemctl status pythonfile.service

echo "uninstalling libre office.."

sudo apt-get remove --purge libreoffice* -y
sudo apt-get clean -y
sudo apt-get autoremove -y
sudo apt --fix-broken install -y

export DISPLAY=:1
xrandr -s 1280x1024

vncpasswd

echo "
set ubuntu password:
sudo su -
passwd ubuntu
exit
"
sudo su -

echo "
manual tasks:"
echo "
ubuntu 18, 2gb ram instance, 
-set screen resolution to 1280x1024
-firefox, block video and audio, use Disable HTML5 Autoplay plugin 
-right click bottom bar and delete toolbar
-log in to both yt and tt
-set firefox zoom to 70%, both on tiktok and youtube (both upload page and channel page)
-set youtube account language to english
-start an upload with selecting file from desktop folder 
instance inbound rule: click instance, click security, click security group ("sg-00 [...]"), edit inbound rules, add rule, type all traffic, source custom, 0.0.0.0/0
- make sure no changes were made that keep repo from being pulled
- make sure there's no files in the desktop
"

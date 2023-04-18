#!/bin/bash

sudo apt-get update  -y
echo "installing mate.."
#sudo apt-get install x2goserver x2goserver-xsession -y
sudo apt install tasksel  -y
sudo tasksel install ubuntu-mate-desktop  -y
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

sudo apt install python3-pip  -y
python3.8 -m pip install -U --force-reinstall pip
python3.8 -m pip install mss pyautogui serial opencv-python keyboard pyKey
sudo apt-get install python3-tk python3-dev  -y
#sudo apt-get install pypy-dev

echo "setting up aws python service.."

sudo cat /etc/systemd/system/pythonfile.service

echo  -e '[Unit]\nDescription=python_aws\nAfter=multi-user.target\n\n[Service]\nType=simple\nUser=ubuntu\nEnvironment="DISPLAY=:1"\nWorkingDirectory=/home/ubuntu/aws-python/\nExecStart=/usr/bin/python3.8 /home/ubuntu/aws-python/aws-side.py\n\n[Install]\nWantedBy=multi-user.target'  | sudo tee /etc/systemd/system/pythonfile.service

sudo systemctl daemon-reload && sudo systemctl enable pythonfile.service && sudo systemctl start pythonfile.service && sudo systemctl status pythonfile.service

echo "uninstalling libre office.."

sudo apt-get remove --purge libreoffice* -y
sudo apt-get clean
sudo apt-get autoremove
sudo apt --fix-broken install

export DISPLAY=:1
xrandr -s 1280x1024

vncpasswd

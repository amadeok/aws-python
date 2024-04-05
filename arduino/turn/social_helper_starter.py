


import time, random, subprocess, psutil
import ArdClick
ac = ArdClick.ardclick.ardclick()
ac.init()
ac.ard.close()

# Function to close the process if it is running
def close_if_running(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.kill()
            while  any(proc.name() == process_name for proc in psutil.process_iter()):
                print(f"waiting {process_name} to close..")
                time.sleep(0.3)


resolve_bin = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
ld_player_bin = r"C:\LDPlayer\LDPlayer9\dnplayer.exe"

close_if_running("Resolve.exe")

close_if_running("dnplayer.exe")

resolve_running = any(proc.name() == "Resolve.exe" for proc in psutil.process_iter())

ld_player_running = any(proc.name() == "dnplayer.exe" for proc in psutil.process_iter())

if not resolve_running:
    print("Starting resolve ....")
    resolve = subprocess.Popen(resolve_bin)

if not ld_player_running:
    print("Starting ldplayer....")
    ld  = subprocess.Popen(ld_player_bin)

if not resolve_running:
    resolve.wait()
    print("resolve has terminated ....")
else:
    print("resolve is already running ....")

if not ld_player_running:
    ld.wait()
    print("ldplayer has terminated ....")
else:
    print("ldplayer is already running ....")

time.sleep(2)
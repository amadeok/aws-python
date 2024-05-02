


import time, random, subprocess, psutil, os
import dotenv
import provision
import ArdClick
import arduino.turn.arduino_helper as arduino_helper
import app_logging
import logging
from datetime import datetime, timedelta
from utils.provision_utils import gs, round_time, calculate_times_per_day, print_debug_setup_times, print_time_setup, break_down_delta, break_down_time_settings

dotenv.load_dotenv()

def close_if_running(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.kill()
            while  any(proc.name() == process_name for proc in psutil.process_iter()):
                logging.info(f"waiting {process_name} to close..")
                time.sleep(0.3)

def connect_arduino(arduino_port):
    ac = arduino_helper.arduinoHelper(port=arduino_port)
    ac.ar.init() #will raise exception if arduino not found, preventing script from going further
    ac.ar.ard.close()
    return ac


def start_processes():
    global resolve_running
    global ld_player_running
    global resolve
    global ld
    resolve_bin = os.getenv("RESOLVE_BIN") #r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
    ld_player_bin = os.getenv("LD_BIN") #r"C:\LDPlayer\LDPlayer9\dnplayer.exe"

    close_if_running("Resolve.exe")

    close_if_running("dnplayer.exe")

    resolve_running = any(proc.name() == "Resolve.exe" for proc in psutil.process_iter())

    ld_player_running = any(proc.name() == "dnplayer.exe" for proc in psutil.process_iter())

    if not resolve_running:
        logging.info("Starting resolve ....")
        resolve = subprocess.Popen(resolve_bin)

    if not ld_player_running:
        logging.info("Starting ldplayer....")
        ld  = subprocess.Popen(ld_player_bin)

def wait_for_processes():
    global resolve_running
    global ld_player_running
    global resolve
    global ld
    if not resolve_running:
        resolve.wait()
        logging.info("resolve has terminated ....")
    else:
        logging.info("resolve is already running ....")

    if not ld_player_running:
        ld.wait()
        logging.info("ldplayer has terminated ....")
    else:
        logging.info("ldplayer is already running ....")



if __name__ == "__main__":
    arduino_port = os.getenv("ARDUINO_PORT")

    ac = connect_arduino(arduino_port)

    start_processes()

    time.sleep(2)

    database = provision.do_provision()

    #wait_for_processes()

    uploads_per_day, upload_time_offset, upload_frequency, minimum_upload_frequency_h = break_down_time_settings(database) #minimum_upload_frequency_h
    
    print_time_setup(uploads_per_day, upload_time_offset, upload_frequency, minimum_upload_frequency_h)

    #print_debug_setup_times(upload_time_offset, upload_frequency)

    date=  datetime.now()
    
    rup = round_time(date, upload_frequency*60, mode="up", offset_minutes=( upload_time_offset)*60)
    
    logging.info(f"""Current time: {date.strftime("%d-%m-%Y %H:%M")}""")
    
    delta = rup-date if rup>date else date-rup
    
    years, months, days, hours, minutes, string = break_down_delta(delta)

    logging.info(f"""Next scheduled upload session time: {rup.strftime("%d-%m-%Y %H:%M")} in {string}""") 

    ac.ar.init()
    ac.set_turn_on_interval(delta.seconds//60)
    ac.get_board_data()
    ac.ar.ard.close()

    turn_off = int(os.getenv("TURN_OFF_PC_AFTER_UPLOAD"))
    if turn_off:
        logging.info("Turning off pc in 30 seconds")
        os.system("shutdown /s /t 30")

    logging.info("Script terminated")



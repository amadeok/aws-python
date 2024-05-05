


import sys, os
import dotenv
dotenv.load_dotenv()
sys.path.insert(0, os.getenv("RESOLVE_PYTHON_PATH") )
import time, random, subprocess, psutil
import provision
import ArdClick
import arduino.turn.arduino_helper as arduino_helper
import app_logging
import logging
from datetime import datetime, timedelta
from utils.provision_utils import gs, round_time, calculate_times_per_day, print_debug_setup_times, print_time_setup, break_down_delta, break_down_time_settings



def connect_arduino(arduino_port):
    ac = arduino_helper.arduinoHelper(True, port=arduino_port)
    #ac.ar.init() #will raise exception if arduino not found, preventing script from going further
    #ac.ar.ard.close()
    
    ac.ar.init()
    ac.set_board_mode(ac.boardModeEnum.mouseKeyboard.value)
    ac.ar.change_delay_between(250) #250ms for click

    return ac



def wait_for_processes(vars):
    resolve_running, ld_player_running, resolve, ld = vars
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

    #processes = start_processes()

    time.sleep(2)

    database,processes = provision.do_provision(ac)

    #wait_for_processes(vars)

    uploads_per_day, upload_time_offset, upload_frequency, minimum_upload_frequency_h = break_down_time_settings(database) #minimum_upload_frequency_h
    
    print_time_setup(uploads_per_day, upload_time_offset, upload_frequency, minimum_upload_frequency_h)

    #print_debug_setup_times(upload_time_offset, upload_frequency)

    date=  datetime.now()
    
    rup = round_time(date, upload_frequency*60, mode="up", offset_minutes=( upload_time_offset)*60)
    
    logging.info(f"""Current time: {date.strftime("%d-%m-%Y %H:%M")}""")
    
    delta = rup-date if rup>date else date-rup
    
    years, months, days, hours, minutes, string = break_down_delta(delta)

    logging.info(f"""Next scheduled upload session time: {rup.strftime("%d-%m-%Y %H:%M")} in {string}""") 

    #ac.ar.init()
    ac.set_turn_on_interval(delta.seconds//60)
    ac.get_board_data()
    ac.set_board_mode(ac.boardModeEnum.standard.value)
    ac.ar.ard.close()

    turn_off = int(os.getenv("TURN_OFF_PC_AFTER_UPLOAD"))
    if turn_off:
        mins = 3
        logging.info(f"Turning off pc in {mins} mins")
        os.system(f"shutdown /s /t {mins*60}")

    logging.info("Script terminated")



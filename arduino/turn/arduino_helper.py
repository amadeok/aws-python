

#import serial
from enum import Enum
import math
import time, random
#import autopyBot
import pyautogui
import msvcrt, serial
import logging

#a = autopyBot.autopy.autopy(r"F:\all\GitHub\aws-python\arduino\turn\imgs")
import ArdClick

#ac = start(False)
#ac.write_custom(updateIntervalCode, [90])
# ac.write_custom(setBeepOnBlink, [0])
#exit()
#ac.reboot()

def map_number(num, from_min, from_max, to_min, to_max):
    # Normalize the number within the given range
    normalized_num = (num - from_min) / (from_max - from_min)
    # Map the normalized number to the target range
    mapped_num = normalized_num * (to_max - to_min) + to_min
    return mapped_num
    
class arduinoHelper():
    class boardModeEnum(Enum):
        standard = 0
        mouseKeyboard = 1
    
    updateIntervalCode =  40010
    setBeepOnBlink =  40011
    getVars =  40012
    setBoardMode = 40009
    def __init__(self, reset_arduino=False, port=None) -> None:
        self.ar = ArdClick.ardclick.ardclick(reset_arduino=reset_arduino, port=port)
    
    def set_turn_on_interval(self, interval):
        self.ar.write_custom(self.updateIntervalCode, [interval])
    
    def set_beep_on_blink(self, val):
        self.ar.write_custom(self.setBeepOnBlink, [val])
        
    def set_board_mode(self, val):
        self.ar.write_custom(self.setBoardMode, [val])
        
    def get_board_data(self):
        self.ar.write_custom(self.getVars, [0])
    
        # ret = self.ar.ard.read_all()#read(120)
        # if len(ret) != 120:
        #     logging.info(f"WARNING RET SIZE != 120: {len(ret)}")
        received_bytes = bytearray()
        t0 = time.time()
        while len(received_bytes) < 120:
            # Read bytes from the serial port
            bytes_to_read = min(120 - len(received_bytes), self.ar.ard.in_waiting)  # Ensure not to read more than needed or available
            received_bytes += self.ar.ard.read(bytes_to_read)
        logging.info(f"receive took {(time.time() - t0):4.3f}")
        labels = ["intervalMins", "targetMs",  "elapsedMs",  "remMs",  "hours",  "minutes",  "tensOfMinutes",  "millis (sec)"]
        for x in range(len(labels)):
            integer_value = int.from_bytes(received_bytes[x*4:(x+1)*4], byteorder='little')
            logging.info(f"{str(labels[x]).ljust(20)} {integer_value}")
            
#    def mouse_move_s(self, point, x_of=0, y_of=0): 
    def move_mouse_s(self, target, x_of=0, y_of= 0, start=None, duration=None, randomness=10, recursive=True, end_randomness=1):
        self.ar.move_mouse_s(target, x_of, y_of, start, duration, randomness, recursive, end_randomness)
        return
        def apply_randomness(integer, randomness):
            min_value = integer - randomness
            max_value = integer + randomness
            return random.randint(min_value, max_value)
        
        start_x, start_y = start if start else pyautogui.position()
        if len(target) > 2: target = target[0:2]
        end_x, end_y = [apply_randomness(int(e), end_randomness) for e in target]
        end_x += int(x_of)
        end_y += int(y_of)
        if duration == None:
            dis =  math.sqrt((start_x - end_x)**2 + (start_y - end_y)**2)
            duration = map_number(dis, 0, 2202,  0, 0.65)

        num_steps = max(1,  int(duration * 100))
        step_x = (end_x - start_x) / num_steps
        step_y = (end_y - start_y) / num_steps
        #pyautogui.mouseDown()
        for i in range(num_steps):
            perc = (((num_steps-i))/num_steps) *2
            randomness_ =  randomness*min(perc, 1) 
            x = start_x + step_x * i + random.uniform(-randomness_, randomness_)
            y = start_y + step_y * i + random.uniform(-randomness_, randomness_)
            #pyautogui.moveTo(x, y)
            #logging.info(randomness,randomness_, perc)
            self.ar.mouse_move((int(x), int(y)))
            #time.sleep(duration / num_steps)
        #if recursive: #self.move_mouse(pos.x, pos.y, end_x, end_y, 0.2, 0, False)
        for x in range(2):
            self.ar.mouse_move((end_x, end_y))
            pos = pyautogui.position()
            logging.info(pos)
        #logging.info(f"dur {duration} steps {num_steps}")
        self.ar.write_mouse_coor_new((end_x, end_y))
        #pyautogui.mouseUp()                                                                           
                                       

                                 
if __name__ == "__main__":
    ac = arduinoHelper(1, "COM7")

    ac.ar.init()
    ac.set_board_mode(ac.boardModeEnum.mouseKeyboard.value)
    ac.ar.change_delay_between(40)
    ps = [(500, 500), (1600, 600), (1400,1100), (400, 1000) ]
    while 1:
        for p in ps:#[ps[1]]:
            ac.move_mouse_s(p)

            #ac.move_mouse_s( p, duration=0.5, randomness=10)
            time.sleep(2)
    exit()
    n= 0
    ac.ar.init()
    #ac.set_turn_on_interval(300)
    #ac.ar.ard.close()
    ac.set_beep_on_blink(0)
    ac.set_board_mode(ac.boardModeEnum.mouseKeyboard.value)
    t = 0
    pt = 0
    for x in range(3840):
        pt = t
        t = time.time()
        d = t- pt
        logging.info(f"{ (t- pt):<4.3f}")
        ac.ar.mouse_move((x, 400))
    exit()
    while 1:
        
        ac.ar.init()
        time.sleep(1)
        ac.get_board_data()
        #logging.info(ret)
        if msvcrt.kbhit():
            key = msvcrt.getch().decode()
            if key == '\x1b': #esc
                logging.info("---------> exit",key)
                break
        ac.ar.ard.close()

        # ac.mouse_move((n,n))
        continue
        n+=1
        ac.mouse_move((random.randint(0, 3000), random.randint(0, 2000)))
        time.sleep(0.1)
        if n > 10:break


    
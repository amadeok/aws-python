

#import serial
import time, random
#import autopyBot
import msvcrt, serial

#a = autopyBot.autopy.autopy(r"F:\all\GitHub\aws-python\arduino\turn\imgs")
import ArdClick

#ac = start(False)
#ac.write_custom(updateIntervalCode, [90])
# ac.write_custom(setBeepOnBlink, [0])
#exit()
#ac.reboot()

class arduinoHelper():
    updateIntervalCode =  40010
    setBeepOnBlink =  40011
    getVars =  40012
    def __init__(self, reset_arduino=False, port=None) -> None:
        self.ar = ArdClick.ardclick.ardclick(reset_arduino=False, port=port)
    
    def set_turn_on_interval(self, interval):
        self.ar.write_custom(self.updateIntervalCode, [interval])
    
    def set_beep_on_blink(self, val):
        self.ar.write_custom(self.setBeepOnBlink, [val])
        
    def get_board_data(self):
        self.ar.write_custom(self.getVars, [0])
    
        # ret = self.ar.ard.read_all()#read(120)
        # if len(ret) != 120:
        #     print(f"WARNING RET SIZE != 120: {len(ret)}")
        received_bytes = bytearray()
        t0 = time.time()
        while len(received_bytes) < 120:
            # Read bytes from the serial port
            bytes_to_read = min(120 - len(received_bytes), self.ar.ard.in_waiting)  # Ensure not to read more than needed or available
            received_bytes += self.ar.ard.read(bytes_to_read)
        print(f"receive took {(time.time() - t0):4.3f}")
        labels = ["intervalMins", "targetMs",  "elapsedMs",  "remMs",  "hours",  "minutes",  "tensOfMinutes",  "millis (sec)"]
        for x in range(len(labels)):
            integer_value = int.from_bytes(received_bytes[x*4:(x+1)*4], byteorder='little')
            print(f"{str(labels[x]).ljust(20)} {integer_value}")
            
if __name__ == "__main__":
    ac = arduinoHelper(False, "COM7")
    n= 0
    ac.ar.init()
    ac.set_turn_on_interval(300)
    ac.ar.ard.close()
    while 1:
        
        ac.ar.init()
        time.sleep(1)
        ac.get_board_data()
        #print(ret)
        if msvcrt.kbhit():
            key = msvcrt.getch().decode()
            if key == '\x1b': #esc
                print("---------> exit",key)
                break
        ac.ar.ard.close()

        # ac.mouse_move((n,n))
        continue
        n+=1
        ac.mouse_move((random.randint(0, 3000), random.randint(0, 2000)))
        time.sleep(0.1)
        if n > 10:break


    
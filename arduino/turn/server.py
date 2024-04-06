

#import serial
import time, random
#import autopyBot
import msvcrt

#a = autopyBot.autopy.autopy(r"F:\all\GitHub\aws-python\arduino\turn\imgs")
import ArdClick
ac = ArdClick.ardclick.ardclick()
ac.init()
n= 0
updateIntervalCode =  40010
setBeepOnBlink =  40011
getVars =  40012
#ac.write_custom(updateIntervalCode, [120])

while 1:
    #time.sleep(1)
    
    ac.write_custom(getVars, [3])
    ret = ac.ard.read(120)
    labels = ["intervalMins", "targetMs",  "elapsedMs",  "remMs",  "hours",  "minutes",  "tensOfMinutes",  "millis (sec)"]
    for x in range(len(labels)):
        integer_value = int.from_bytes(ret[x*4:(x+1)*4], byteorder='little')
        print(f"{str(labels[x]).ljust(20)} {integer_value}")

    #print(ret)
    if msvcrt.kbhit():
        key = msvcrt.getch().decode()
        if key == '\x1b': #esc
            print("---------> exit",key)
            break

    # ac.mouse_move((n,n))
    continue
    n+=1
    ac.mouse_move((random.randint(0, 3000), random.randint(0, 2000)))
    time.sleep(0.1)
    if n > 10:break


 
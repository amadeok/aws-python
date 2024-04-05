#import serial
import time, random
#import autopyBot

#a = autopyBot.autopy.autopy(r"F:\all\GitHub\aws-python\arduino\turn\imgs")
import ArdClick
ac = ArdClick.ardclick.ardclick()
ac.init()
n= 0
updateIntervalCode =  40010
setBeepOnBlink =  40011

while 1:
    ac.write_custom(updateIntervalCode, [2])
    #ac.write_custom(setBeepOnBlink, [0])

    # ac.mouse_move((n,n))
    break
    n+=1
    ac.mouse_move((random.randint(0, 3000), random.randint(0, 2000)))
    time.sleep(0.1)
    if n > 10:break


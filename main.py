import board
import busio
import time

from pixy import *
from sphero_rvr import *

p = Pixy()
rvr = RVRDrive()

setpoint = 30000
k = 0.005

while(True):
    #Search for a block
    p.get_blocks(1,1)
    # if a block is found, print the x, y, width, and height
    # and set the color to green
    if(p.blockFound == True):
        p.set_led(0,255,0)
        #print([p.x,p.y,p.width,p.height])
        error = p.x - setpoint
        output = round(error*k)
        print(output)
        if(output > 255):
            output = 255
        if(output < -255):
            output = -255
        rvr.setMotors(40+output,40-output)

    else:
        p.set_led(255,0,0)

    time.sleep(0.1)



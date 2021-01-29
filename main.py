
import board
import busio
import time

from pixy import *
from sphero_rvr import *

p = Pixy()
rvr = RVRDrive()

MAX_PAN_SERVO = 510
MIN_PAN_SERVO = 0
setpoint = 255
k = 0.1
kI = 0.005
output = 0.0
panSetpoint = 120.0
panSignal = panSetpoint

j = setpoint
accumulatedError = 0.0
while(True):
    #Search for a block
    p.get_blocks(1,1)
    # if a block is found, print the x, y, width, and height
    # and set the color to green


    if(p.blockFound == True):
        p.set_led(0,255,0)
        #print([p.x,p.y,p.width,p.height])
        panError = panSetpoint - p.x
        output = k*panError + kI*accumulatedError
        panSignal += output
        accumulatedError += panError
        if(panSignal > MAX_PAN_SERVO):
            panSignal = MAX_PAN_SERVO
        if(panSignal < MIN_PAN_SERVO):
            panSignal = MIN_PAN_SERVO
        p.set_servo(round(panSignal),255)
        print(panSignal)
        '''
        if(output > 255):
            output = 255
        if(output < -255):
            output = -255
        rvr.setMotors(70+output,70-output)
        '''
    else:
        p.set_led(255,0,0)
        #rvr.setMotors(0,0)
        panSignal += 5.0
        accumulatedError = 0.0
        p.set_servo(round(panSignal),255)
        if(panSignal > 511):
            panSignal = 0

        if(j>511):
            j = 0



    time.sleep(0.02)

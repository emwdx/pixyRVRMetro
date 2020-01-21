import board
import busio
import digitalio
import time
import pulseio
import struct

uart = busio.UART(board.D1, board.D0, baudrate=115200)

i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_bus_device.i2c_device import I2CDevice


#Code below is from the sphero.py API file.
'''
class LEDs:
    RIGHT_HEADLIGHT = [0x00, 0x00, 0x00, 0x07]
    LEFT_HEADLIGHT = [0x00, 0x00, 0x00, 0x38]
    LEFT_STATUS = [0x00, 0x00, 0x01, 0xC0]
    RIGHT_STATUS = [0x00, 0x00, 0x0E, 0x00]
    BATTERY_DOOR_FRONT = [0x00, 0x03, 0x80, 0x00]
    BATTERY_DOOR_REAR = [0x00, 0x00, 0x70, 0x00]
    POWER_BUTTON_FRONT = [0x00, 0x1C, 0x00, 0x00]
    POWER_BUTTON_REAR = [0x00, 0xE0, 0x00, 0x00]
    LEFT_BRAKELIGHT = [0x07, 0x00, 0x00, 0x00]
    RIGHT_BRAKELIGHT = [0x38, 0x00, 0x00, 0x00]


class RawMotorModes:
    OFF = 0
    FORWARD = 1
    BACKWARD = 2
'''

class RVRDrive:
    @staticmethod
    def drive(speed, heading):

        flags = 0x00

        if speed < 0:
            speed *= -1
            heading += 180
            heading %= 360
            flags = 0x01

        drive_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x07, 0x00,
            speed, heading >> 8, heading & 0xFF, flags
        ]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        uart.write(bytearray(drive_data))

        return

    @staticmethod
    def stop(heading):
        RVRDrive.drive(0, heading)

        return

    @staticmethod
    def set_raw_motors(left_mode, left_speed, right_mode, right_speed):
        if left_mode < 0 or left_mode > 2:
            left_mode = 0

        if right_mode < 0 or right_mode > 2:
            right_mode = 0

        raw_motor_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x01, 0x00,
            left_mode, left_speed, right_mode, right_speed
        ]

        raw_motor_data.extend([~((sum(raw_motor_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        uart.write(bytearray(raw_motor_data))

        return

    @staticmethod
    def reset_yaw():
        drive_data = [0x8D, 0x3E, 0x12, 0x01, 0x16, 0x06, 0x00]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        uart.write(bytearray(drive_data))

        return

#Code below is commented to reduce space to run on the Metro. Otherwise we get a MemoryError.

'''
class RVRLed:
    @staticmethod
    def set_all_leds(red, green, blue):
        led_data = [
            0x8D, 0x3E, 0x11, 0x01, 0x1A, 0x1A, 0x00,
            0x3F, 0xFF, 0xFF, 0xFF
        ]

        for _ in range (10):
            led_data.extend([red, green, blue])

        led_data.extend([~((sum(led_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        uart.write(bytearray(led_data))

        return

    @staticmethod
    def set_rgb_led_by_index(index, red, green, blue):
        led_data = [0x8D, 0x3E, 0x11, 0x01, 0x1A, 0x1A, 0x00]

        led_data.extend(index)
        led_data.extend([red, green, blue])
        led_data.extend([~((sum(led_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        uart.write(bytearray(led_data))

        return


class RVRPower:
    @staticmethod
    def wake():
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x0D, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        uart.write(bytearray(power_data))

        return

    @staticmethod
    def sleep():
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x01, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        uart.write(bytearray(power_data))

        return

'''

#The Pixy2 code is based on the work of Robert Lucian. Code here: https://github.com/RobertLucian/pixy2


class Pixy2():


    def __init__(self, i2c, address):
        self.address = address
        self.i2c_device = I2CDevice(i2c, address)
        self.blocks = []


    def set_lamp(self, on):
        '''
        Turn on or off the Pixy2's lamp.

        :param on: True or False on whether the Pixy2's lamps is on or off.
        :return: Nothing.
        '''

        with self.i2c:
            out = [174, 193, 22, 2, 1 if on else 0, 0]
            for msg in out:
                self.i2c_device.write(bytes(out), stop=False)


    def set_led(self, red, green, blue):
        """
        Set the Pixy2's RGB LED.

        :param red: 0-255.
        :param green: 0-255.
        :param blue: 0-255.
        :return: Nothing
        """
        out = [174, 193, 20, 3, red, green, blue]

        with self.i2c_device:
            self.i2c_device.write(bytes(out), stop=False)

    #Code below is commented out to save space.

    '''
    def get_resolution(self):
        """
        Return the width and height of the camera.

        :return: width, height (0-511). None if the checksum didn't match.
        """
        out = [
            # 2 sync bytes, type packet, length payload, unused type
            174, 193, 12, 1, 0
        ]
        with self.i2c_device:
            self.i2c_device.write(bytes(out), stop = False)
            inp = bytearray(10)
            self.i2c_device.readinto(inp)
            checksum = struct.unpack('<H', bytes(inp[4:6]))[0]
            if checksum == sum(inp[6:10]):
                width, height = struct.unpack('<HH', bytes(inp[6:10]))
                return width, height
            else:
                return None

    def get_version(self):
            """
            Get the hardware and software version of the Pixy2.

            :return: hw, sw
            """
            out = [
                # 2 sync bytes, type packet, length payload
                174, 193, 14, 0
            ]
            print('get version from pixy2')
            with self.i2c_device:
                self.i2c_device.write(bytes(out), stop = False)
                inp = bytearray(14)
                self.i2c_device.readinto(inp)

                #hw = unpack_bytes(inp[6:8], big_endian=False)
                hw = struct.unpack('H', bytes(inp[6:8]))[0]
                major = inp[8]
                minor = inp[9]
                #build = unpack_bytes(inp[10:12], big_endian=False)
                build = struct.unpack('H', bytes(inp[10:12]))[0]
                fw_type = inp[12]
                fw = '{}.{}.{}-{}'.format(major, minor, build, chr(fw_type))
                return hw, fw
    def get_fps(self):
            """
            Get the Pixy2's camera FPS.

            :return: The FPS as an integer.
            """
            out = [
                # 2 sync bytes, type packet, length payload
                174, 193, 24, 0
            ]
            #print('get fps from pixy2')
            with self.i2c_device:

                self.i2c_device.write(bytes(out), stop = False)
                inp = bytearray(10)
                self.i2c_device.readinto(inp)

                fps = struct.unpack('<I', bytes(inp[6:10]))[0]

            return fps

    '''

    def get_blocks(self, sigmap, maxblocks):
        """
        Get detected blocks from the Pixy2.

        :param sigmap: Indicates which signatures to receive data from.
        0 for none, 255 for all, all the rest it's in between.
        :param maxblocks: Maximum blocks to return.
        0 for none, 255 for all of them, all the rest it's in between.
        :return: signature, X center of block (px) (0-315), Y center of block (px) (0-207), width
        of block (px) (0-316), height of block (px) (0-208), angle of color-code in degrees (-180 - 180)
        w/ 0 if not a color code, tracking index (0-255), age or the number of frames this
        block has been tracked for (0-255) - it stops incrementing at 255. Returned as a list of pairs.
        :return: None if it hasn't detected any blocks or if the process has encountered errors.
        """
        out = [ 174, 193, 32, 2, sigmap, maxblocks]
         # 2 sync bytes, type packet, length payload,
         # sigmap, max blocks to return
        #print('detect pixy2 blocks')
        with self.i2c_device:
            self.i2c_device.write(bytes(out), stop=False)
            result = bytearray(20)

            self.i2c_device.readinto(result)

            #for msg in result:
            #    print(int(msg))
            type_packet = result[2]

            if type_packet == 33:
                payload_length = result[3]

                inp = result[4:]


                checksum = struct.unpack('<H', bytes(inp[0:2]))[0]

                if(checksum == sum(inp[2:])):
                    block_length = 14
                    num_blocks = payload_length // block_length
                    blocks = []

                    if(num_blocks > 0):
                        for i in range(num_blocks):
                            data = struct.unpack('<5HhBB', bytes(inp[(i*block_length+2):(i+1)*block_length+2]))
                            blocks.append(data)
                        #print('pixy2 detected {} blocks'.format(no_blocks))
                        self.blocks = blocks[0]

                    else:
                        self.blocks = []
                    return self.blocks


            else:
                #print('checksum doesn\'t match for the detected blocks')
                self.blocks = []
                return None

        #print('pixy2 is busy or got into an error while reading blocks')
        #self.blocks = []
        return None
    def isTracking(self):
        if(len(self.blocks)>0):
            return True
        return False

#This was a data structure to better contain tracking information for driving.
class TrackingData():
    def __init__(self, block):
        if(block != None):
            self.x = block[1]/315.0 #number from 0.0 to 1.0
            self.y = block[2]/207.0 #number from 0.0 to 1.0
            self.width = block[3] #pixels
            self.height = block[4] #pixels

        else:
            self.x = None #number from 0.0 to 1.0
            self.y = None #number from 0.0 to 1.0
            self.width = None #pixels
            self.height = None #pixels

#Setting up the Pixy at its default address of 0x54
myPixy = Pixy2(i2c, 0x54)

#This is a visual confirmation that I2C is working by flashing the LEDs.
myPixy.set_led(255, 0,0)
time.sleep(0.1)
myPixy.set_led(0, 255,0)
time.sleep(0.1)
myPixy.set_led(0, 0,255)
time.sleep(0.1)
myPixy.set_led(0, 0,0)
time.sleep(0.1)

#Driving constants
kP = 25.0
maxAngle = 10.0
outputAngle = 1.0

#Create an RVR object to use in driving
rvr = RVRDrive()

while True:

    try:
        tracked_object = TrackingData(myPixy.get_blocks(255,1))

        #if there is an object in the camera view:
        if(tracked_object.x != None):
            #The yaw reset is to turn off the heading drive
            rvr.reset_yaw()
            print("x: {} y: {} height: {} width: {} ".format(tracked_object.x, tracked_object.y, tracked_object.width, tracked_object.height))


            outputAngle = (tracked_object.x - 0.5)*kP

            if(outputAngle>maxAngle):
                outputAngle = maxAngle
            elif(outputAngle<-maxAngle):
                outputAngle = -maxAngle
            outputAngleRounded = int(outputAngle)
            if(outputAngle < 0):
                outputAngleRounded = 360 + outputAngleRounded
            print(outputAngleRounded)
            rvr.drive(30,outputAngleRounded)
            time.sleep(0.1)
        else:
            rvr.stop(0)
            time.sleep(0.1)
    except:
        print("error")



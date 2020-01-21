# pixyRVRMetro
Code to get a Pixy2 driving a Sphero RVR through CircuitPython running on an Adafruit Metro.

##Usage

The Pixy2 is connected to the Metro using the SCL/SDA pins, ground, and 5V.

The Metro is connected to the RVR serial RX, GND, and 5V Pins. The 5V out of the RVR connects to Vin of the Metro and GND is connected to the Metro GND. The RX pin is tied to the RX pin of the Metro (Pin 1).

The Sphero code is almost the same as the micro:bit api code in sphero.py, but the UART is replaced with CircuitPython code to use the serial port of the Metro.

The Pixy code is based on Robert Lucian's Python implementation of the Pixy2 API which can be found at https://github.com/RobertLucian/pixy2



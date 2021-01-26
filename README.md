# pixyRVRMetro
Code to get a Pixy2 driving a Sphero RVR through CircuitPython running on an Adafruit Metro.

##Usage

On this branch, the Pixy2 is connected to the Metro using the SPI pins. 

The Metro is connected to the RVR serial RX, GND, and 5V Pins. The 5V out of the RVR connects to Vin of the Metro and GND is connected to the Metro GND. The RX pin is tied to the TX pin of the Metro (Pin 2).

The Sphero code is almost the same as the micro:bit api code in sphero.py, but the UART is replaced with CircuitPython code to use the serial port of the Metro.

The Pixy code was initially based on Robert Lucian's Python implementation of the Pixy2 API (found at https://github.com/RobertLucian/pixy2) .T his was changed to address the difference in how the packets are sent over SPI. 



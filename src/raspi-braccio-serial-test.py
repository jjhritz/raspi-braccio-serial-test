"""
Module: raspi-braccio-serial-test
Project: raspi-braccio-serial-test
Description: Test the response of a Tinkertoy Braccio robot arm controlled from a Raspberry Pi via USB connection.
Assumes commands are compliant with the sketch in this repo: https://github.com/jjhritz/BraccioSerialControlTest

Date: 10/16/2018
Author: John J. Hritz
Email: john-j-hritz@sbcglobal.net
"""

import serial
import platform
import random
import time
from threading import Timer

random.seed()

unoBaudRate = 9600
unoCOM = 'COM10'                # COM port the Uno is connected to on Windows
unotty = '/dev/ttyACM0'         # tty device the Uno is connected to on Linux
commandInterval = 0.05             # how often commands are sent, in seconds


# Class code shamelessly lifted from: https://code.i-harness.com/en/q/bdbf0b
class perpetualTimer:

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


if platform.system() is "Linux":
    arduinoSerialData = serial.Serial(unotty, unoBaudRate)

if platform.system() is "Windows":
    arduinoSerialData = serial.Serial(unoCOM, unoBaudRate)


def send_command():
    # command = input("Enter command in the form <uint,uint,int>: ")

    # generate command for the arm; out-of-bounds entries will be handled by the sketch
    command = "<" + str(random.randint(0, 5)) + "," + "1" + ","
    command += str(random.randrange(-10, 11, 20)) + ">"
    print(command)

    arduinoSerialData.write(command.encode('utf-8'))


if __name__ is "__main__":
    commandTimer = perpetualTimer(commandInterval, send_command)

    # Only send the command every 5 seconds
    commandTimer.start()
    time.sleep(6)

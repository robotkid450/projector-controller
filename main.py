#!/usr/bin/env python3

import serial
#import tkinter as tk

ser = serial.Serial('/dev/ttyUSB0', baudrate=19200)

print(ser.name)
ser.write(b'hello')
ser.close()

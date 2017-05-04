#!/usr/bin/env python3
import serial
import sys
import time


def _readline(serialCon):
    # reads from input buffer until it reaches '\r' (carage return)
    msg = ''
    #time.sleep(.1)
    charsAvalible = serialCon.in_waiting
    for num in range(charsAvalible):
        char = serialCon.read().decode()
        if char != '\x0D':
            msg = msg + char
        else:
            break

    return msg


power = 0
lamp1 = '57'
lamp2 = '999'

a = serial.Serial(port=sys.argv[1], baudrate=19200)
while True:
    if a.in_waiting > 0:
        line = _readline(a)
        print('line', line)
        if line == 'C00':
            print('power on')
            global power
            power = 1
            a.write('\x06\r'.encode())
    
        if line == 'C01':
            print('power off')
            global power
            power = 0
            a.write('\x06\r'.encode())
    
        if line == 'CR0':
            print(power)
            if power == 0:
                a.write('01\r'.encode())
                print('power off send')
            else:
                a.write('00\r'.encode())
                print('power on send')
                
        if line == 'CR3':
            lhour = lamp1 + ' ' + lamp2 + '\r'
            a.write(lhour.encode())
            print(lhour)
            print('lamp hour send')
            
                
        
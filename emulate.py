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
vidin = 1
lamp1 = '57'
lamp2 = '999'

a = serial.Serial(port=sys.argv[1], baudrate=19200)
while True:
    time.sleep(.1)
    if a.in_waiting > 0:
        line = _readline(a)
        print('line', line)
        
        # change status from power on
        if line == 'C00':
            print('power on')
            #global power
            power = 1
            a.write('\x06\r'.encode())
    
        # change status from power off
        if line == 'C01':
            print('power off')
            #global power
            power = 0
            a.write('\x06\r'.encode())
            
        # set input 1
        if line == 'C05':
            print('input 1')
            vidin = 1
            a.write('\x06\r'.encode())
            
        # set input 2
        if line == 'C06':
            print('input 2')
            vidin = 2
            a.write('\x06\r'.encode())
            
        # set input 3
        if line == 'C07':
            print('input 3')
            vidin = 3
            a.write('\x06\r'.encode())
            
        
            
        
        #gen stat
        if line == 'CR0':
            print(power)
            if power == 0:
                a.write('01\r'.encode())
                print('power off send')
            else:
                a.write('00\r'.encode())
                print('power on send')
        
        if line == 'CR1':
            a.write(str(vidin).encode())

        # lamp Hours
        if line == 'CR3':
            lhour = lamp1 + ' ' + lamp2 + '\r'
            a.write(lhour.encode())
            print(lhour)
            print('lamp hour send')
            
                
        
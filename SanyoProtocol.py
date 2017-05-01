#!/usr/bin/env python3

import time
import serial

class projector:
    def __init__(self, port="/dev/ttyUSB0", baudrate=19200):
        self.serialPort = port
        self.serialBaudrate = baudrate
        self.serialIs_connected = 0
        self.ackSize = 2

    def _connect(self):
        try:
            self.serialCon = serial.Serial(
                port=self.serialPort, baudrate=self.serialBaudrate, timeout=3)
        except:
            self.serialIs_connected = 0
            print("error _connecting to device")
        else:
            self.serialIs_connected = 1

    def _disconnect(self):
        try:
            self.serialCon.close()
        except:
            self.serialIs_connected = -1
            print("error disconecting ??")
        else:
            print("serial disconected")
            self.serialIs_connected = 0

    def _sendCommandControl(self, command):
        # build command string
        commandToSend = "C" + str(command) + '\r'
        # encode commandToSend
        commandToSend = commandToSend.encode()

        # write commandToSend to serial port
        try:
            self.serialCon.write(commandToSend)
        except:
            print("error writing to port" + '\n\r' + "check that cable?")
        else:
            print("data written")

    def _sendCommandRead(self, command, bytesToRecv):
        # build command string
        commandToSend = "CR" + str(command) + '\r'
        # encode commandToSend
        commandToSend = commandToSend.encode()

        try:
            self.serialCon.write(commandToSend)
        except:
            print("error writing to port" + '\n\r' + "check that cable?")
        else:
            print("data written")

        retunCode = self._recvData(bytesToRecv)

        self._disconnect()

    def _readline(self):
        msg = ''
        time.sleep(.1)
        charsAvalible = self.serialCon.in_waiting
        for num in range(charsAvalible):
            char = self.serialCon.read().decode()
            if char != '\x0D':
                msg = msg + char
            else:
                break

        return msg

    def _getAck(self):
        ack = self._readline()
        if ack == '\x06':
            return 0
        elif ack == '?':
            print("Invalid command")
            return 1
        else:
            print("Unknown error")
            return -1

    def powerOn(self):
        self._connect()
        self._sendCommandControl('00')
        self._getAck()
        self._disconnect()

    def powerOff(self):
        self._connect()
        self._sendCommandControl('01')
        self._getAck()
        self._disconnect()

    def setInput(self, videoInput):
        videoInput = videoInput + 4 # increments for command offset: input 1 = c05
        print(videoInput)
        videoInput = '0' + str(videoInput)
        self._connect()
        self._sendCommandControl(videoInput)
        self._getAck()
        self._disconnect()

    def autoAdjust(self):
        self._connect()
        self._sendCommandControl('89')
        self._getAck()
        self._disconnect()

#!/usr/bin/env python3

import time
import serial

__version__ = '1.0'

class projector:
    def __init__(self, port="/dev/ttyUSB0", baudrate=19200):
        self.serialPort = port
        self.serialBaudrate = baudrate
        self.serialIsConnected = 0
        self.commandDelay = .1
        self.statusCodeGeneral = ''
        self.currentInput = 0
        self.lampHours = -1

    def _connect(self):
        # connects serial port
        try:
            self.serialCon = serial.Serial(
                port=self.serialPort, baudrate=self.serialBaudrate, timeout=3)
        except:
            self.serialIsConnected = 0
            print("error connecting to device")
        else:
            self.serialIsConnected = 1

    def _disconnect(self):
        # disconects serial port
        try:
            self.serialCon.close()
        except:
            self.serialIsConnected = -1
            print("error disconecting ??")
        else:
            print("serial disconected")
            self.serialIsConnected = 0

    def _readline(self):
        # reads from input buffer until it reaches '\r' (carage return)
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

    def _sendCommandControl(self, command):
        # sends a control command to projector
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

        time.sleep(self.commandDelay)

        ack = self._getAck()

        return ack

    def _sendCommandRead(self, command):
        # sends a read command to projector and return status message
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

        time.sleep(self.commandDelay)

        returnCode = self._readline()

        return returnCode

    def _getAck(self):
        # checks if control commands were sent correctly
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
        # powers on the projector
        self._connect()
        status = self._sendCommandControl('00')
        self._disconnect()
        return status

    def powerOff(self):
        # powers off the projector
        self._connect()
        status = self._sendCommandControl('01')
        self._disconnect()
        return status

    def setInput(self, videoInput):
        # sets the video input of the projector
        videoInput = int(videoInput) + 4 # increments for command offset: input 1 = c05
        print(videoInput)
        videoInput = '0' + str(videoInput)
        self._connect()
        status = self._sendCommandControl(videoInput)
        self._disconnect()
        return status

    def autoAdjust(self):
        # runs the projectors autoAdjust function
        self._connect()
        status = self._sendCommandControl('89')
        self._disconnect()
        return status

    def getStatusGeneral(self):
        # polls projector for its general status. returns string
        self._connect()
        status = self._sendCommandRead('0')
        if status == '?':
            print('error getting status')
        else:
            self.statusCodeGeneral = status

        self._disconnect()

        return status

    def getLampHour(self):
        # polls projector for its current lamp Hours. Returns a list of 1 to 4 int
        self._connect()
        rawHours = self._sendCommandRead('3')
        if rawHours == '?':
            print('error getting lamp hours')
        else:
            rawHours = str(rawHours)
            Hours = rawHours.split(' ')
            self.lampHours = Hours

        self._disconnect()

        return Hours

    def getInput(self):
        # polls projector of current input. returns int
        self._connect()
        rawInput = self._sendCommandRead('1')
        if rawInput == '?':
            print('error getting status')
        else:
            videoInput = int(rawInput)
            self.currentInput = videoInput

        self._disconnect()

        return videoInput

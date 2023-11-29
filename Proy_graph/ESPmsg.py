
# Code2
# ------------------------------------------------------------------------------------
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import serial 
import serial.tools.list_ports as portList 

from serialCoder import SerialCoder

import numpy as np 
import ctypes
import csv
import time
import random 
import array as arr
import struct 
import string 

from enum import Enum, auto 

SERIAL_FRAME_SYNC1 = 0
SERIAL_FRAME_SYNC2 = 1
SERIAL_FRAME_ID = 2
SERIAL_FRAME_VALUE = 3
SERIAL_FRAME_CRC = 4
SERIAL_FRAME_LENGHT = 5



poly = 0x04C11DB7

class State (Enum):
    IdleDisconnected = auto()
    IdleConnected = auto()
    InSession = auto()

class RxState(Enum):
    Sync1 = auto()
    Sync2 = auto()
    PacketType1 = auto()
    Payload = auto()
    CRC = auto()

class ParserState (Enum):
    Type = auto()
    Size = auto()
    CRC = auto()
    payload = auto()

class SystemState:
    def __init__(self):
        self.__state = State.IdleDisconnected

    def setState(self, state):
        self.__state = state

    def getState(self):
        return self.__state

class MySignal(qtc.QObject):
    sig = qtc.pyqtSignal(object, object)

class WorkerThread(qtc.QThread):
    def __init__(self, s, sCoder, parent=None):
        qtc.QThread.__init__(self, parent)
        self.s = s
        self.sCoder = sCoder
        self.exiting = False
        self.rxstate = RxState.Sync1
        self.signal = MySignal()
        self.crc = 255
        self.message = list()
        self.type = 0
        self.payload = 0
        self.txArray = [0,0,0,0,0]

        self.crcTable = [
        0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 
        0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, 
        0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 
        0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d, 
        0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 
        0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, 
        0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 
        0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, 
        0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 
        0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, 
        0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 
        0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, 
        0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 
        0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a, 
        0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 
        0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a, 
        0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 
        0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4, 
        0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 
        0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, 
        0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 
        0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, 
        0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 
        0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, 
        0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 
        0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63, 
        0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 
        0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, 
        0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 
        0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, 
        0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 
        0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3 
        ]

        super().__init__()

    def calculateCRC8(self, data, length):
        print("calculating")
        crc = 0x00
        for i in range (length):
            crc = self.crcTable[crc ^ data[i]]
            #print(crc)
        return crc

    @qtc.pyqtSlot()
    def run(self):
        try:
            while not self.exiting:
                try:
                    if(self.rxstate == RxState.Sync1):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"sync1 : {hex(dataRead)}")
                        if(dataRead == 0xA5):
                            self.rxstate = RxState.Sync2
                            self.message.append(dataRead)
                        else:
                            self.rxstate = RxState.Sync1
                    elif(self.rxstate == RxState.Sync2):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"sync2 : {hex(dataRead)}")
                        if(dataRead == 0x5A):
                            self.rxstate = RxState.PacketType1
                            self.message.append(dataRead)
                        else:
                            self.rxstate = RxState.Sync1
                    elif(self.rxstate == RxState.PacketType1):
                        dataRead = self.sCoder.read_u08(self.s)
                        if(dataRead != 0):
                            print(f"type : {hex(dataRead)}")
                            self.rxstate = RxState.Payload
                            self.type = dataRead
                            self.message.append(dataRead)
                       
                    elif(self.rxstate == RxState.Payload):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"payload : {hex(dataRead)}")
                        self.payload = dataRead
                        self.message.append(dataRead)
                        self.rxstate = RxState.CRC  
                    elif(self.rxstate == RxState.CRC):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"crc arrives: {hex(dataRead)}")
                        print(self.message)
                        self.crc = self.calculateCRC8(self.message, len(self.message))
                        print(f"crc calculated: {self.crc}")
                        if(dataRead == self.crc):
                            self.signal.sig.emit(self.type, self.payload)    
                        self.message.clear()
                        self.rxstate = RxState.Sync1
                           
                except:
                    dataRead = {}
        finally:
            print("not running")
    
    def encodeMesage(self, id, value):
        self.txArray[SERIAL_FRAME_SYNC1] = 0xA5
        self.txArray[SERIAL_FRAME_SYNC2] = 0x5A
        self.txArray[SERIAL_FRAME_ID] = id
        self.txArray[SERIAL_FRAME_VALUE] = value
        self.txArray[SERIAL_FRAME_CRC] = self.calculateCRC8(self.txArray, 4)
    
    def sendMessage(self):
        for i in self.txArray:
            self.sCoder.write_u08(self.s,i)
            print(hex(i))







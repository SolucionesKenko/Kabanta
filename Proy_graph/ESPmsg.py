
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

custom_crc_table = {}
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
        self.type = 0
        self.payload = 0

        super().__init__()

    @qtc.pyqtSlot()
    def run(self):
        try:
            while not self.exiting:
                try:
                    if(self.rxstate == RxState.Sync1):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"sync1 : {dataRead}")
                        if(dataRead == 0xA5):
                            self.rxstate = RxState.Sync2
                        else:
                            self.rxstate = RxState.Sync1
                    elif(self.rxstate == RxState.Sync2):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"sync2 : {dataRead}")
                        if(dataRead == 0x5A):
                            self.rxstate = RxState.PacketType1
                        else:
                            self.rxstate = RxState.Sync1
                    elif(self.rxstate == RxState.PacketType1):
                        dataRead = self.sCoder.read_u08(self.s)
                        if(dataRead != 0):
                            print(f"type : {dataRead}")
                            self.rxstate = RxState.Payload
                            self.type = dataRead
                       
                    elif(self.rxstate == RxState.Payload):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"payload : {dataRead}")
                        self.payload = dataRead
                        self.rxstate = RxState.CRC  
                    elif(self.rxstate == RxState.CRC):
                        dataRead = self.sCoder.read_u08(self.s)
                        print(f"crc : {dataRead}")
                        if(dataRead == 0):
                            self.signal.sig.emit(self.type, self.payload)    
                        self.rxstate = RxState.Sync1
                           
                except:
                    dataRead = {}
        finally:
            print("not running")







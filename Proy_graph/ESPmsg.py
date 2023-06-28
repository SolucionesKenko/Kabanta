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
    sig = qtc.pyqtSignal(object)

class WockerThread(qtc.QThred):
    def __init__(self, s, sCoder, parent=None):
        qtc.QThread.__init__(self, parent)
        self.s = s
        self.sCoder = sCoder
        self.exiting = False
        self.bytesToRead = 0
        self.rxstate = RxState.Sync1
        self.signal = MySignal()

        super().__init__()

    @qtc.pyqtSlot()
    def run(self):
        try:
            while not self.exiting:
                try:
                    if(self.rxstate == RxState.Sync1):
                        dataRead = self.sCoder.read_u08(self.s)
                        if(dataRead == 0xAA):
                            self.rxstate = RxState.Sync2
                        else:
                            self.rxstate = RxState.Sync1
                    elif(self.rxstate == RxState.Sync2):
                        dataRead = self.sCoder.read_u08(self.s)
                        if(dataRead == 0x55):
                            self.rxstate = RxState.PacketType1
                        else:
                            self.rxstate = RxState.Sync1
                    elif(self.rxstate == RxState.PacketType1):
                        dataRead = self.sCoder.read_u16(self.s)
                        self.rxstate = RxState.Payload
                        self.signal.sig.emit(dataRead)
                    elif(self.rxstate == RxState.Payload):
                        dataRead = self.s.read(self.bytesToRead)
                        self.bytesToRead = 0
                        self.signal.sig.emit(dataRead)
                        self.rxstate = RxState.Sync1  
                    elif(self.rxstate == RxState.CRC):
                        dataRead = self.sCoder.read_u32(self.s)
                        self.rxstate = RxState.Payload
                        self.signal.sig.emit(dataRead)       
                except:
                    dataRead = {}
        finally:
            print("not running")






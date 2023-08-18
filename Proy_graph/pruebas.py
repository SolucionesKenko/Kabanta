from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg 
import sys 
import numpy as np
from data_test import ecg_signal, obtainSignals
from window import Ui_window
from collections import deque
from StylesheetFormat import PressedStylesheet, Stylesheet
import pandas as pd
# Manejo de puertos
import serial 
import serial.tools.list_ports as portList 
#from Bluetooth Variables
from ESPmsg import ParserState, WorkerThread, State
from serialCoder import SerialCoder

from enum import Enum, auto, IntEnum
import spo
import co2
import bp
spo = spo.SPO()
co2 = co2.CO2()
bp =bp.BloodPressure()
from time import time


generateSig = obtainSignals()
ecg12 = generateSig.generateSignals(60)

rsp = list(generateSig.generate_rsp())
pokemon = [1,2,3,4,5,6,7,8]
pokemon2 = pd.DataFrame(pokemon)[0]
print(pokemon[:2000])
print(deque(pokemon + list(pokemon2+10)[-3:],maxlen=12))




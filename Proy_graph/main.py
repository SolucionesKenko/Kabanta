### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore
#import pyqtgraph as pg 
import sys 
import numpy as np
from data_test import ecg_signal, obtainSignals
from window import Ui_window

# Manejo de puertos
import serial 
import serial.tools.list_ports as portList 
#from Bluetooth Variables
from ESPmsg import ParserState, WorkerThread, State
from serialCoder import SerialCoder
# Manejo de arreglos en la senal 
# todo, cambiar el manejo de datos con collections deque
from collections import deque
from itertools import cycle


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_window()
        self.ui.setupUi(self)
        #self.bt = DeviceFinder()
        #self.bt.startDeviceDiscovery()
        
        #Session
        self.crcErrorCounter = 0
        self.sessionToken = 0
        self.sessionSequence = 0
        self.sequenceArray = np.zeros(shape=[1,1])
        self.commandToken = 0

        # Data Variables
        self.mi_diccionario = {"1":75,"2":0,"3":0,"4":0,"5":0,"6":0}
        self.generateSig = obtainSignals()
        self.ecg12 = self.generateSig.generateSignals(self.mi_diccionario["1"])
        
        self.parserState = ParserState.Type
        self.crc = 0
        self.type = 0
        self.size = 0
        self.pendingPayload = 0
        self.sequence = 0
        self.sessionToken = 0
        self.responseCode = 0
        self.originPacketType = 0
        self.OriginToken = 0
        self.moduleError = 0
        self.sn = 0
        self.rate = 0
        self.channelMask = 0
        self.messageInBytes = []
        #self.timer=qtc.QTimer()

        # Connections
        self.s = ""
        self.sCoder = SerialCoder()
        self.sPorts = list(portList.comports())
        self.addPorts()
        self.sConnected = False
        self.exceptionCnt = 0
        self.packetOffset = 0
        self.mcuError = 0
        self.temp = 0
        self.vref = 0
        self.adcOvr = 0
        self.serialOvr = 0
        self.crcMismatches = 0
        self.spiOverrun = 0
        self.moduleList = ['GPIO','UART','SPI','FLASH','IWDG','ADC','ADS1299','EEPROM','SERIAL','SIGNAL_ACQ','SIGNAL_PROC','NVS','SETTINGS','COMMANDS','DATA','SESSION','SYSTEM','CLOCK','CRC']
        self.errorList = ['NONE','NO_INIT','WRONG_PARAM','BUSY','PERIPH_FAILURE','COMPONENT_FAILURE','UNKNOWN_FAILURE','UNKNOWN_COMPONENT','BUS_FAILURE','CLOCK_FAILURE','MSP_FAILURE','FEATURE_NOT_SUPPORTED','TIMEOUT']
        self.custom_crc_table = {}
        self.poly = 0x04C11DB7
        self.generate_crc32_table(self.poly)

        #Button Control
        self.Ui_window = Ui_window()
        self.ui.DEFIB_pushButton.pressed.connect(self.displayHello)
        self.ui.Charge_pushButton.pressed.connect(self.displayHello)
        self.ui.Shock_pushButton.pressed.connect(self.displayHello)
        self.ui.DEA_pushButton.pressed.connect(self.displayHello)
        self.ui.SYNC_pushButton.pressed.connect(self.displayHello)
        # Confirm es connect y return es scan 
        self.ui.confirmMenu_pushButton.pressed.connect(self.onConnectConfirmButtonClicked)
        self.ui.returnMenu_pushButton.pressed.connect(self.onScanReturnButtonClicked)

        self.ui.alarmMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.CPRMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.sizeMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.LEADMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.DPO_pushButton.pressed.connect(self.displayHello)
        self.ui.DPR_pushButton.pressed.connect(self.displayHello)
        self.ui.UPO_pushButton.pressed.connect(self.displayHello)
        self.ui.UPR_pushButton.pressed.connect(self.displayHello)
        self.ui.config_pushButton.pressed.connect(self.Pokemon)
        self.ui.UpEnergySelect_pushButton.pressed.connect(self.displayHello)
        self.ui.DownEnergySelect_pushButton.pressed.connect(self.displayHello)
        self.ui.play_RoundButton.pressed.connect(self.displayHello)
        self.ui.pause_RoundButton.pressed.connect(self.displayHello)
        self.ui.stop_RoundButton.pressed.connect(self.displayHello)
        self.ui.question_RoundButton.pressed.connect(self.displayHello)
        self.ui.OnOff_RoundButton.pressed.connect(self.displayHello)
        self.ui.UpRoundTriangle.pressed.connect(self.displayHello)
        self.ui.DownRoundTriangle.pressed.connect(self.displayHello)

        ### Final de configuracion de los Widgets
        ### Codigo de main
        #Agregados al Layout vertical
        self.initSignalGrahps()
        #Actualizacion de grafica
        self.su = 1
        self.timer = QtCore.QTimer()
        self.timer.setInterval(2)
        self.timer.timeout.connect(self.update_Grahp)
        self.timer.start()
        # User code starts Here 

    def Pokemon(self):
        print("inicio")
        print("final")

    ### Funciones Iniciales 
    def initSignalGrahps(self):
        #Eje en x 
        self.x = list(range(500))
        np.zeros
        # Senales Derivaciones cardiacas
        self.der1 = [0 for i in self.x]
        self.der2 = [-2 for i in self.x]
        self.der3 = [-4 for i in self.x]
        #todo pen =
        self.data_line_der1 = self.ui.plt.plot(self.x,self.der1)
        self.data_line_der2 = self.ui.plt.plot(self.x,self.der2)
        self.data_line_der3 = self.ui.plt.plot(self.x,self.der3)
        # User code end Here 

    def update_Grahp(self):
        # todo cambiar el manejo de datos con collections deque
        self.su = self.su + 1
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.der1 = self.der1[1:]  # Remove the first
        self.signalBufferDer1 = cycle(self.ecg12['I'])
        self.der1.append(self.signalBufferDer1[self.su])  # Add a new random value.
        

        self.der2 = self.der2[1:]  # Remove the first
        self.signalBufferDer2 = cycle(self.ecg12['II'])
        self.der2.append(self.signalBufferDer2[self.su]-2)  # Add a new random value.

        self.der3 = self.der3[1:]  # Remove the first
        self.signalBufferDer3 = cycle(ecg_signal[self.su])
        self.der3.append(self.signalBufferDer3[2]-4)  # Add a new random value.

        self.data_line_der1.setData(self.x, self.der1)  # Update the data.
        self.data_line_der2.setData(self.x, self.der2)
        self.data_line_der3.setData(self.x, self.der3)
        
    def Update_Grahp(self):
        # todo cambiar el manejo de datos con collections deque
        self.su = self.su + 1
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.der1 = self.der1[1:]  # Remove the first
        self.der1.append(self.ecg12['I'][self.su])  # Add a new random value.
        

        self.der2 = self.der2[1:]  # Remove the first
        self.der2.append(self.ecg12['II'][self.su]-2)  # Add a new random value.

        self.der3 = self.der3[1:]  # Remove the first
        self.der3.append(ecg_signal[self.su][2]-4)  # Add a new random value.

        self.data_line_der1.setData(self.x, self.der1)  # Update the data.
        self.data_line_der2.setData(self.x, self.der2)
        self.data_line_der3.setData(self.x, self.der3)

    def displayHello(self):
        print("hello")

    # Funciones bluetooth
    
    def addPorts(self):
        for p in self.sPorts:
            print(p[0])
            self.ui.port_comboBox.addItem(p[0])
        print("New ports added")
    
    def generate_crc32_table(self, _poly):
        for i in range(256):
            c = i << 24
            for j in range(8):
                c = (c << 1) ^ _poly if (c & 0x80000000) else c << 1
            self.custom_crc_table[i] = c & 0xffffffff

    def onScanReturnButtonClicked(self):
        print("Scan On")
        self.sPorts.clear()
        self.sPorts = list(portList.comports())
        self.ui.port_comboBox.clear()
        self.addPorts()

    def onConnectConfirmButtonClicked(self):
        self.s = serial.Serial(
            self.ui.port_comboBox.currentText(), baudrate=115200, timeout=100)

        self.sConnected = self.s.is_open
        if(self.sConnected):
            print("Conectado")
            self.state = (State.IdleConnected)
            self.worker = WorkerThread(self.s, self.sCoder)
            self.worker.exiting = False
            self.state = State.IdleConnected
            self.worker.signal.sig.connect(self.testWorker)
            self.worker.start()
    
    def testWorker(self, id, data):
        print(f"id {id}")
        print(f"value : {data}")
        # Cambiar diccionario
        self.mi_diccionario[f"{id}"] = data
        print(self.mi_diccionario)

    #def updateDiccionario(self):

        





main_Stylesheet = """
#Pokemon {
    background-color: rgb(209,209,209);
    }

"""






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(main_Stylesheet)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

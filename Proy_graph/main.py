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
from collections import deque

# Manejo de puertos
import serial 
import serial.tools.list_ports as portList 
#from Bluetooth Variables
from ESPmsg import ParserState, WorkerThread, State
from serialCoder import SerialCoder

from enum import Enum, auto, IntEnum
import spo
# Manejo de arreglos en la senal 
# todo, cambiar el manejo de datos con collections deque

class SignalState (Enum):
    Playing = auto()
    Pause = auto()
    Stop = auto()
    Idle = auto()

HEART_RATE = "1"
TEMPERATURE = "2"
SPO = "3"
SYSPRESSURE = "4"
DIAPRESSURE = "5"
FR = "6"
CO = "7"

class PageState (IntEnum):
    OFFPAGE = 0
    DEFAULTPAGE = 1
    CPRPAGE = 2
    DEFIBPAGE = 3
    PACERPAGE = 4

    



class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_window()
        self.ui.setupUi(self)
        
        #Session
        self.signalState = SignalState.Idle
        self.state = State.IdleDisconnected
        self.pageState = PageState.OFFPAGE

        # Data Variables
        self.mi_diccionario = {HEART_RATE:0,TEMPERATURE:0,SPO:0,SYSPRESSURE:0,DIAPRESSURE:0,FR:0, CO:0}
        self.generateSig = 0
        self.ecg12 = 0
        self.i = 0
        self.parserState = ParserState.Type
        self.spo = spo.SPO()
        self.i_rsp = 0
        self.adder = 0
        # Manejo de tiempos
        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime()
        self.elapsedTime = QtCore.QElapsedTimer()

        # Connections
        self.s = ""
        self.sCoder = SerialCoder()
        self.sPorts = list(portList.comports())
        self.addPorts()
        self.sConnected = False
        self.custom_crc_table = {}
        self.poly = 0x04C11DB7
        self.generate_crc32_table(self.poly)
        self.r = deque()

        #Button Control
        self.ui.DEFIB_pushButton.pressed.connect(self.onDEFIBButtonClicked)
        self.ui.Charge_pushButton.pressed.connect(self.displayHello)
        self.ui.Shock_pushButton.pressed.connect(self.displayHello)
        self.ui.DEA_pushButton.pressed.connect(self.displayHello)
        self.ui.SYNC_pushButton.pressed.connect(self.displayHello)
        # Confirm es connect y return es scan 
        self.ui.confirmMenu_pushButton.pressed.connect(self.onConnectConfirmButtonClicked)
        self.ui.returnMenu_pushButton.pressed.connect(self.onScanReturnButtonClicked)

        self.ui.alarmMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.CPRMenu_pushButton.pressed.connect(self.onCPRButtonClicked)
        self.ui.sizeMenu_pushButton.pressed.connect(self.onPacerButtonClicked)
        self.ui.LEADMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.DPO_pushButton.pressed.connect(self.displayHello)
        self.ui.DPR_pushButton.pressed.connect(self.displayHello)
        self.ui.UPO_pushButton.pressed.connect(self.displayHello)
        self.ui.UPR_pushButton.pressed.connect(self.displayHello)
        self.ui.config_pushButton.pressed.connect(self.displayHello)
        self.ui.UpEnergySelect_pushButton.pressed.connect(self.displayHello)
        self.ui.DownEnergySelect_pushButton.pressed.connect(self.displayHello)
        self.ui.play_RoundButton.pressed.connect(self.onPlayButtonClicked)
        self.ui.pause_RoundButton.pressed.connect(self.onPauseButtonClicked)
        self.ui.stop_RoundButton.pressed.connect(self.onStopButtonClicked)
        self.ui.question_RoundButton.pressed.connect(self.displayHello)
        self.ui.OnOff_RoundButton.pressed.connect(self.onOnOffButtonClicked)
        self.ui.UpRoundTriangle.pressed.connect(self.displayHello)
        self.ui.DownRoundTriangle.pressed.connect(self.displayHello)

        ### Final de configuracion de los Widgets
        ### Codigo de main
        # Inicializacion de las senales de las graficas
        self.initSignalGrahps()
    

    ##########################################################################################
    # Funtiones del Interfaz Grafica (GUI)
    def initSignalGrahps(self):
        #Eje en x 
        self.x = list(range(500))
        # Senales Derivaciones cardiacas
        #self.der1 = [0 for i in self.x]
        self.channel1 = [-0 for i in self.x]
        self.channel2 = [-4 for i in self.x]
        self.channel3 = [-8 for i in self.x]
        self.channel4 = [-12 for i in self.x]
        self.channel5 = [-16 for i in self.x]
        
        self.data_line_ppg = self.ui.plt.plot(pen = (134,234,233))
        self.data_line_rsp = self.ui.plt.plot(pen = (255,222,89))
        self.data_line_channel1 = self.ui.plt.plot(self.x,self.channel1, pen = (162,249,161))
        self.data_line_channel2 = self.ui.plt.plot(self.x,self.channel2, pen = (162,249,161))
        self.data_line_channel3 = self.ui.plt.plot(self.x,self.channel3, pen = (162,249,161))
        
        # Futuro inicializacion de senales
        # self.data_line_channel4 = self.ui.plt.plot(self.x,self.channel4, pen = (134,234,233))
        # self.data_line_channel5 = self.ui.plt.plot(self.x,self.channel5, pen = (255,222,89))

    def onPlayButtonClicked(self):
        
        if(self.signalState == SignalState.Idle):
            self.setDefaultValues()
            self.generateSig = obtainSignals()
            self.ecg12 = self.generateSig.generateSignals(self.mi_diccionario[HEART_RATE])
            self.rsp = list(self.generateSig.generate_rsp())
            self.time.__init__(0,0,0,0)
        
        if(self.signalState != SignalState.Playing):
            self.ui.heartRateValue_Label.setText(str(self.mi_diccionario[HEART_RATE]))
            self.ui.tempValue_Label.setText(str(self.mi_diccionario[TEMPERATURE]))
            self.ui.SpO2Value_Label.setText(str(self.mi_diccionario[SPO]))
            self.ui.pressureValue_Label.setText(str(self.mi_diccionario[SYSPRESSURE]))
            self.ui.pressureValue_Label.setText(str(self.mi_diccionario[DIAPRESSURE]))
            self.ui.FRValue_Label.setText(str(self.mi_diccionario[FR]))
            self.ui.CO2Value_Label.setText(str(self.mi_diccionario[CO]))

            # ReInicializacion de la senal posterior a SignalState.Stop
            if(self.signalState == SignalState.Stop):
                self.initSignalGrahps()
            
            self.signalState = SignalState.Playing
            print(self.signalState)
            # Envio de estado por serial 
            if self.state != State.IdleDisconnected:
                self.worker.encodeMesage(8,1)
                self.worker.sendMessage()
            
            # Manejo de timer y time
            self.elapsedTime.start()
            self.timer.setInterval(2)
            self.timer.timeout.connect(self.Update_Grahp)
            self.timer.timeout.connect(self.Update_Time)
            self.timer.start()

    def onPauseButtonClicked(self):
        
        self.timer.stop()
        self.signalState = SignalState.Pause
        print(self.signalState)
        # Envio de estado por serial 
        if self.state != State.IdleDisconnected:
            self.worker.encodeMesage(8,2)
            self.worker.sendMessage()
        
    def onStopButtonClicked(self):
        
        self.timer.stop()
        self.setDefaultValues()
        self.ui.plt.clear()
        self.adder = 0
        self.signalState = SignalState.Stop
        print(self.signalState)

        # Envio de estado por serial 
        if self.state != State.IdleDisconnected:
            self.worker.encodeMesage(8,3)
            self.worker.sendMessage()
            
    def onOnOffButtonClicked(self):
        if self.pageState != PageState.OFFPAGE:
            self.pageState = PageState.OFFPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.OFFPAGE)
            
        else:
            self.pageState = PageState.DEFAULTPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)

    def onCPRButtonClicked(self):
        if self.pageState != PageState.OFFPAGE:
            self.pageState = PageState.CPRPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.CPRPAGE)
    
    def onDEFIBButtonClicked(self):
        if self.pageState != PageState.OFFPAGE:
            self.pageState = PageState.DEFIBPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFIBPAGE)

    def onPacerButtonClicked(self):
        if self.pageState != PageState.OFFPAGE:
            self.pageState = PageState.PACERPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.PACERPAGE)
            

    def Update_Grahp(self):
        if(self.adder >= len(self.ecg12['I'])-1):
            self.adder = 0
        if(self.i_rsp >= 9999):
            self.i_rsp = 0
        while(self.i > 499):
            self.i = self.i - 1
            self.r.popleft()

        self.adder = self.adder + 1
        self.i_rsp = self.i_rsp + 1
        self.i = self.i + 1
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.channel1 = self.channel1[1:]                   # Remove the first
        self.channel1.append(self.ecg12['I'][self.adder])   # Add a new random value.

        self.channel2 = self.channel2[1:]                   # Remove the first
        self.channel2.append(self.ecg12['II'][self.adder]-4)# Add a new random value.

        self.channel3 = self.channel3[1:] 
        self.channel3.append(self.ecg12["III"][self.adder]-8)  # Add a new random value.

        self.r.append((self.rsp[self.i_rsp])-12)

        self.spo.update_plot()
        self.data_line_rsp.setData(self.x, self.r)
        self.data_line_ppg.setData(self.x, list(self.spo.dataIR)[1:])
        self.data_line_channel1.setData(self.x, self.channel1)
        self.data_line_channel2.setData(self.x, self.channel2)
        self.data_line_channel3.setData(self.x, self.channel3)


    ##########################################################################################
    # Funciones Para el manejo del tiempo  

    def Update_Time(self):
        self.updateElapsedTime()
        self.ui.simulationTimeValue_pushButton.setText(str(self.elapsed_time))
    
    def updateElapsedTime(self):
        self.elapsed_time = self.time.addMSecs(self.elapsedTime.elapsed()).toString("hh:mm:ss")

    def displayHello(self):
        print("hello")

    ##########################################################################################
    # Funciones serial
    
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
            self.ui.port_comboBox.currentText(), baudrate=115200, timeout=500)

        self.sConnected = self.s.is_open
        if(self.sConnected):
            print("Conectado")
            self.state = (State.IdleConnected)
            self.worker = WorkerThread(self.s, self.sCoder)
            self.worker.exiting = False
            self.state = State.IdleConnected # Es correcto que el state sea conectado
            self.worker.signal.sig.connect(self.testWorker)
            self.worker.start()
    
    def setDefaultValues(self):
        self.mi_diccionario = {HEART_RATE:60,TEMPERATURE:36,SPO:98,SYSPRESSURE:60,DIAPRESSURE:80,FR:25, CO:25}

    def updateUI(self, id, data):
        if(id == HEART_RATE):
            self.ui.heartRateValue_Label.setText(str(data))
            self.ecg12 = self.generateSig.generateSignals(self.mi_diccionario[HEART_RATE])
        elif(id == TEMPERATURE):
            self.ui.tempValue_Label.setText(str(data))
        elif(id == SPO):
            self.ui.SpO2Value_Label.setText(str(data))
        elif(id == SYSPRESSURE):
            self.ui.pressureValue_Label.setText(str(data))
        elif(id == DIAPRESSURE):
            self.ui.pressureValue_Label.setText(str(data))
        elif(id == FR):
            self.ui.FRValue_Label.setText(str(data))
        elif(id == CO):
            self.ui.CO2Value_Label.setText(str(data))
        else:
            print("Invalid ID")

    def testWorker(self, id, data):
        # Cambiar diccionario
        s_id = str(id)
        self.mi_diccionario[s_id] = data
        print(self.mi_diccionario)
        self.updateUI(s_id, data)

    


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

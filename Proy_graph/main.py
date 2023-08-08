### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg 
import sys 
import numpy as np
from data_test import ecg_signal, obtainSignals
from window import Ui_window
from collections import deque
from StylesheetFormat import PressedStylesheet, Stylesheet

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

from time import time
# Manejo de arreglos en la senal 
# todo, cambiar el manejo de datos con collections deque

class SignalState (Enum):
    Playing = auto()
    Pause = auto()
    Stop = auto()
    Idle = auto()

class DEFIBState(Enum):
    Off = auto()
    Select = auto()
    Charging = auto()
    Charged = auto()
    Shock = auto()

class WorkingState(Enum):
    Busy = auto()
    Idle = auto()

class ScenarioState(IntEnum):
    Idle = 0
    ParoCardiaco = 1
    TaquicardiaSinusal = 2
    BradicardiaSinusal = 3 
    FlutterAuricular = 4
    FibrilacionAuricular = 5
    TaquicardiaAuricular = 6
    ArritmiaSinusal = 7
    FibrilacionVentricular = 8
    TaquicardiaVentricular = 9
    Asistolia = 10
    

HEART_RATE = "1"
TEMPERATURE = "2"
SPO = "3"
SYSPRESSURE = "4"
DIAPRESSURE = "5"
FR = "6"
CO = "7"
SCENARIO = "8"

PACEMAKER_MA = "1"
PACEMAKER_PPM = "2"
DEFIB_SELECT = "3"
DEFIB_CHARGE = "4"

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
        self.graphlength = 2000
        
        #Session
        self.signalState = SignalState.Idle
        self.state = State.IdleDisconnected
        self.pageState = PageState.OFFPAGE
        self.defibState = DEFIBState.Off
        self.workingState = WorkingState.Idle
        self.scenarioState = ScenarioState.Idle

        # Data Variables
        self.mi_diccionario = {HEART_RATE:0,TEMPERATURE:0,SPO:0,SYSPRESSURE:0,DIAPRESSURE:0,FR:0, CO:0}
        self.mi_pagevariables = {PACEMAKER_MA:18, PACEMAKER_PPM:70,DEFIB_SELECT:0,DEFIB_CHARGE:0}
        self.generateSig = 0
        self.ecg12 = 0
        self.i = 0
        self.parserState = ParserState.Type
        self.spo = spo.SPO()
        self.co2 = co2.CO2()
        self.bp =bp.BloodPressure()

        self.dataChannel1 = 0
        self.dataChannel2 = 0
        self.dataChannel3 = 0
        self.dataChannel4 = 0
        self.dataChannel5 = 0
        self.dataChannel6 = 0
        
        self.adderChannel1 = 0
        self.adderChannel4 = 0
        self.adderChannel5 = 0
        self.adderChannel6 = 0
        
        # Manejo de tiempos
            # Timers 
        self.timer = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
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

        #Button Control
        self.ui.DEA_pushButton.pressed.connect(self.displayHello)
        self.ui.SYNC_pushButton.pressed.connect(self.displayHello)
        # Confirm es connect y return es scan 
        self.ui.confirmMenu_pushButton.pressed.connect(self.onConnectConfirmButtonClicked)
        self.ui.returnMenu_pushButton.pressed.connect(self.onScanReturnButtonClicked)

        self.ui.alarmMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.CPRMenu_pushButton.pressed.connect(self.onCPRButtonClicked)
        self.ui.sizeMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.LEADMenu_pushButton.pressed.connect(self.displayHello)
        # Pacer 
        self.ui.DPO_pushButton.pressed.connect(self.onPacerOutputDownButtonClicked)
        self.ui.UPO_pushButton.pressed.connect(self.onPacerOutputUpButtonClicked)
        self.ui.DPR_pushButton.pressed.connect(self.onPacerRateDownButtonClicked)
        self.ui.UPR_pushButton.pressed.connect(self.onPacerRateUpButtonCliked)
        self.ui.pacerLabel_pushButton.pressed.connect(self.onPacerButtonClicked)
        # Defib 
        self.ui.DEFIB_pushButton.pressed.connect(self.onDEFIBButtonClicked)
        self.ui.Charge_pushButton.pressed.connect(self.onChargeButtonClicked)
        self.ui.Shock_pushButton.pressed.connect(self.onShockButtonClicked)
        self.ui.UpEnergySelect_pushButton.pressed.connect(self.onUpEnergySelectButtonClicked)
        self.ui.DownEnergySelect_pushButton.pressed.connect(self.onDownEnergySelectButtonClicked)
        self.ui.DISCHARGE_pushButton.pressed.connect(self.onDischargeButtonClicked)

        self.ui.config_pushButton.pressed.connect(self.displayHello)
        self.ui.play_RoundButton.pressed.connect(self.onPlayButtonClicked)
        self.ui.pause_RoundButton.pressed.connect(self.onPauseButtonClicked)
        self.ui.stop_RoundButton.pressed.connect(self.onStopButtonClicked)
        self.ui.question_RoundButton.pressed.connect(self.displayHello)
        self.ui.OnOff_RoundButton.pressed.connect(self.onOnOffButtonClicked)
        self.ui.UpRoundTriangle.pressed.connect(self.scenDefalt)
        self.ui.DownRoundTriangle.pressed.connect(self.scenExperiment)
        
            
        ### Final de configuracion de los Widgets
        ### Codigo de main
        # Inicializacion de las senales de las graficas
        self.initSignalGrahps()
    

    ##########################################################################################
    # Funtiones del Ploteo Grafica (PUI)
    def initSignalGrahps(self):
        #Eje en x 
        self.x = deque(np.linspace(0,4,self.graphlength),maxlen=self.graphlength)
        # Senales Derivaciones cardiacas
        self.channel1 = deque([130 for i in self.x],maxlen=self.graphlength)
        self.channel2 = deque([110 for i in self.x],maxlen= self.graphlength)
        self.channel3 = deque([90 for i in self.x],maxlen=self.graphlength)
        self.channel4 = deque([70 for i in self.x], maxlen=self.graphlength)
        self.channel5 = deque([50 for i in self.x], maxlen=self.graphlength)
        self.channel6 = deque([30 for i in self.x], maxlen=self.graphlength)

        self.data_line_channel1 = self.ui.plt.plot(self.x,self.channel1, pen = (162,249,161))
        self.data_line_channel2 = self.ui.plt.plot(self.x,self.channel2, pen = (162,249,161))
        self.data_line_channel3 = self.ui.plt.plot(self.x,self.channel3, pen = (162,249,161))
        self.data_line_channel4 = self.ui.plt.plot(self.x,self.channel4, pen = (134,234,233))
        self.data_line_channel5 = self.ui.plt.plot(self.x,self.channel5, pen = (136,51,64))
        self.data_line_channel6 = self.ui.plt.plot(self.x, self.channel6, pen = (255,222,89))
        self.data_line_co2 = self.ui.plt.plot(self.x,[10]*self.graphlength, pen = (171,171,171), fillLevel = -0.3, brush=(171,171,171, 60))
        
        
        # getting plot item
        self.ui.plt.getPlotItem().hideAxis('left')
        self.plot_size = self.ui.plt.getPlotItem().height()
        self.plot_x = self.ui.plt.getPlotItem().viewGeometry()

        self.ui.plt.setYRange(0, 140)

        self.d1text = pg.TextItem('I', color = (162,249,161))
        self.d1text.setPos(-0.2, 130)
        self.ui.plt.addItem(self.d1text)
        self.d2text = pg.TextItem('II', color = (162,249,161))
        self.d2text.setPos(-0.2, 110)
        self.ui.plt.addItem(self.d2text)
        self.d3text = pg.TextItem('III', color = (162,249,161))
        self.d3text.setPos(-0.2, 90)
        self.ui.plt.addItem(self.d3text)
        self.plethtext = pg.TextItem('Pleth', color = (134,234,233))
        self.plethtext.setPos(-0.3, 70)
        self.ui.plt.addItem(self.plethtext)
        self.prestext = pg.TextItem('ABP', color= (136,51,64))
        self.prestext.setPos(-0.3, 50)
        self.ui.plt.addItem(self.prestext)
        self.resptext = pg.TextItem('Resp', color = (255,222,89))
        self.resptext.setPos(-0.3, 30)
        self.ui.plt.addItem(self.resptext)
        self.co2text = pg.TextItem('CO2', color = (171,171,171))
        self.co2text.setPos(-0.3, 10)
        self.ui.plt.addItem(self.co2text)
            
    def signalScenarioData(self):
        if self.scenarioState == ScenarioState.Idle:
            self.dataChannel1 = (self.ecg12['I']*10)
            self.dataChannel2 = (self.ecg12['II']*10)
            self.dataChannel3 = (self.ecg12["III"]*10)
            self.dataChannel4 = list(self.spo.dataIR)
            self.dataChannel5 = list(self.bp.data)
            self.dataChannel6 = (self.rsp)
        elif self.scenarioState == ScenarioState.ParoCardiaco:
            self.dataChannel1 = ([0]*self.graphlength)
            self.dataChannel2 = ([0]*self.graphlength)
            self.dataChannel3 = ([0]*self.graphlength)
            self.dataChannel4 = list(self.spo.dataIR)
            self.dataChannel5 = list([50]*self.graphlength)
            self.dataChannel6 = (self.rsp)



        

    def Update_Grahp(self):
        self.signalScenarioData()
        # Manejo de indices de la senal
        if(self.adderChannel1 >= len(self.dataChannel1)-1):
            self.adderChannel1 = 0
        if (self.adderChannel4 >= len(self.dataChannel4)-1):
            self.adderChannel4 = 0
        if (self.adderChannel5 >= len(self.dataChannel5)-1):
            self.adderChannel5 = 0 
        if(self.adderChannel6 >= len(self.dataChannel6)-1):
            self.adderChannel6 = 0
        
        
        self.adderChannel1 = self.adderChannel1 + 1
        self.adderChannel4 = self.adderChannel4 + 1
        self.adderChannel5 = self.adderChannel5 + 1
        self.adderChannel6 = self.adderChannel6 + 1
        self.i = self.i + 1
        self.x.append(self.x[-1] + 0.002)  # Add a new value 1 higher than the last.

        # Add new values to the channels
        self.channel1.append((self.dataChannel1[self.adderChannel1]) + 130)   
        self.channel2.append(self.dataChannel2[self.adderChannel1]+ 110)
        self.channel3.append(self.dataChannel3[self.adderChannel1] + 90)
        self.channel4.append(self.dataChannel4[self.adderChannel4])
        self.channel5.append(self.dataChannel5[self.adderChannel5])
        self.channel6.append(self.dataChannel6[self.adderChannel6]*10 + 30)
        
        #self.spo.dataIR.rotate(-1)
        
        self.co2.data.rotate(-1)
        
        
        # Actualizacion posicion de labels
        self.d1text.setPos(self.x[0]-0.2, 130)
        self.d2text.setPos(self.x[0]-0.2, 110)
        self.d3text.setPos(self.x[0]-0.2, 90)
        self.plethtext.setPos(self.x[0]-0.3, 70)
        self.prestext.setPos(self.x[0]-0.3, 50)
        self.resptext.setPos(self.x[0]-0.3, 30)
        self.co2text.setPos(self.x[0]-0.3, 10)

        # Actualizacion de los datos
        
        
        self.data_line_co2.setData(self.x, list(self.co2.data)[0:self.graphlength])
        
        self.data_line_channel1.setData(self.x, self.channel1)
        self.data_line_channel2.setData(self.x, self.channel2)
        self.data_line_channel3.setData(self.x, self.channel3)
        self.data_line_channel4.setData(self.x, self.channel4)
        self.data_line_channel5.setData(self.x, self.channel5)
        self.data_line_channel6.setData(self.x, self.channel6)

    ##########################################################################################
    # Funciones Callbacks de botones
    def enableDisableVitalSignalMenu(self,status):
        self.ui.simulationTimeValue_pushButton.setHidden(status)
        self.ui.simulationTimeLabel_Label.setHidden(status)
        self.ui.heartRateLabel_pushButton.setHidden(status)
        self.ui.heartRateValue_Label.setHidden(status)
        self.ui.heartRateUnidades_Label.setHidden(status)
        self.ui.tempLabel_pushButton.setHidden(status)
        self.ui.tempValue_Label.setHidden(status)
        self.ui.tempUnidades_Label.setHidden(status)
        self.ui.SpO2Label_pushButton.setHidden(status)
        self.ui.SpO2Value_Label.setHidden(status)
        self.ui.SpO2Unidades_Label.setHidden(status)
        self.ui.pressureLabel_pushButton.setHidden(status)
        self.ui.pressureValue_Label.setHidden(status)
        self.ui.pressureUnidades_Label.setHidden(status)
        self.ui.FRLabel_pushButton.setHidden(status)
        self.ui.FRValue_Label.setHidden(status)
        self.ui.FRUnidades_Label.setHidden(status)
        self.ui.CO2Label_pushButton.setHidden(status)
        self.ui.CO2Value_Label.setHidden(status)
        self.ui.CO2Unidades_Label.setHidden(status)
        self.ui.roundRectVitalSignals_Qpaint.setHidden(status)
        self.ui.Graph_verticalLayoutWidget.setHidden(status)
        
    def onOnOffButtonClicked(self):
        if self.pageState != PageState.OFFPAGE:
            self.pageState = PageState.OFFPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.OFFPAGE) 
            self.resetKabSim()
            self.resetDefib()
            self.resetPacerPage()
            self.resetCPRPage()
        else:
            self.pageState = PageState.DEFAULTPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)
            self.enableDisableVitalSignalMenu(False)
    
    
    def onPlayButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE):
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
                    if self.pageState != PageState.DEFAULTPAGE:
                        self.ui.plt.removeItem(self.data_line_channel1)
                
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
        if (self.pageState != PageState.OFFPAGE) and (self.signalState == SignalState.Playing) :
            self.timer.stop()
            self.signalState = SignalState.Pause
            print(self.signalState)
            # Envio de estado por serial 
            if self.state != State.IdleDisconnected:
                self.worker.encodeMesage(8,2)
                self.worker.sendMessage()
        
    def onStopButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.signalState != SignalState.Idle):
            self.timer.stop()
            self.setDefaultValues()
            self.ui.plt.clear()
            self.adderChannel1 = 0
            self.adderChannel4 = 0
            self.adderChannel5 = 0
            self.adderChannel6 = 0
            self.signalState = SignalState.Stop
            print(self.signalState)

            # Envio de estado por serial 
            if self.state != State.IdleDisconnected:
                self.worker.encodeMesage(8,3)
                self.worker.sendMessage()
            
    def resetKabSim(self):
        self.enableDisableVitalSignalMenu(True)
        # reseteo de los valores de signos vitales
        self.ui.heartRateValue_Label.setText('- - -')
        self.ui.tempValue_Label.setText('- - -')
        self.ui.SpO2Value_Label.setText('- - -')
        self.ui.pressureValue_Label.setText('- - -')
        self.ui.FRValue_Label.setText('- - -')
        self.ui.CO2Value_Label.setText('- - -')
        self.ui.simulationTimeValue_pushButton.setText('00:00:00')
        # Restablecer timers
        if self.timer.isActive():
            self.timer.stop()
            self.timer.disconnect()
        if self.timer2.isActive():
            self.timer2.stop()
            self.timer2.disconnect()
        # Restablecer graficas
        self.adderChannel1 = 0
        self.adderChannel4 = 0
        self.adderChannel5 = 0
        self.adderChannel6 = 0
        self.i = 0
        self.ui.plt.clear()
        self.initSignalGrahps()
        self.signalState = SignalState.Idle
        self.workingState = WorkingState.Idle
    
    def resetDefib(self):
        self.ui.Shock_pushButton.setStyleSheet(Stylesheet)
        self.ui.DEFIB_pushButton.setStyleSheet(Stylesheet)
        self.ui.Charge_pushButton.setStyleSheet(Stylesheet)
        self.ui.DISCHARGE_pushButton.setStyleSheet(Stylesheet)

    def resetCPRPage(self):
        self.ui.CPRMenu_pushButton.setStyleSheet(Stylesheet)
    def onCPRButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState != PageState.CPRPAGE) and (self.workingState != WorkingState.Busy):
            self.pageState = PageState.CPRPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.CPRPAGE)
            self.ui.CPRMenu_pushButton.setStyleSheet(PressedStylesheet)
            self.resetDefib()
            self.resetPacerPage()
            self.ui.plt.removeItem(self.data_line_channel1)
            print(PageState.CPRPAGE)
        elif (self.pageState != PageState.OFFPAGE) and (self.workingState != WorkingState.Busy):
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)
            self.pageState = PageState.DEFAULTPAGE
            self.resetCPRPage()
            self.data_line_channel1 = self.ui.plt.plot(self.x,self.channel1, pen = (162,249,161))
    
    def onDEFIBButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState != PageState.DEFIBPAGE) and (self.workingState != WorkingState.Busy):
            self.pageState = PageState.DEFIBPAGE
            self.defibState = DEFIBState.Select
            self.ui.plt.removeItem(self.data_line_channel1)
            self.resetPacerPage()
            self.resetCPRPage
            self.mi_pagevariables = {PACEMAKER_MA:18, PACEMAKER_PPM:70,DEFIB_SELECT:0,DEFIB_CHARGE:0}
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFIBPAGE)
            self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_SELECT]} J SEL\nBIFASICO")
            self.ui.DEFIB_pushButton.setStyleSheet(PressedStylesheet)
            print(PageState.DEFIBPAGE)
        elif (self.pageState != PageState.OFFPAGE) and (self.workingState != WorkingState.Busy):
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)
            self.pageState = PageState.DEFAULTPAGE
            # reset page variables
            self.mi_pagevariables[DEFIB_SELECT] = 0
            self.mi_pagevariables[DEFIB_CHARGE] = 0
            self.data_line_channel1 = self.ui.plt.plot(self.x,self.channel1, pen = (162,249,161))
            self.resetDefib()
    
    def onUpEnergySelectButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.DEFIBPAGE) and (self.defibState == DEFIBState.Select):
            if self.mi_pagevariables[DEFIB_SELECT] < 30:
                self.mi_pagevariables[DEFIB_SELECT] = self.mi_pagevariables[DEFIB_SELECT]+5
                self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_SELECT]} J SEL\nBIFASICO")
            else:
                self.mi_pagevariables[DEFIB_SELECT] = self.mi_pagevariables[DEFIB_SELECT]+10
                self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_SELECT]} J SEL\nBIFASICO")
            
            if self.mi_pagevariables[DEFIB_SELECT] != 0:
                self.ui.Charge_pushButton.setStyleSheet(PressedStylesheet)
            else: 
                self.ui.Charge_pushButton.setStyleSheet(Stylesheet)


    def onDownEnergySelectButtonClicked(self):
       if (self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.DEFIBPAGE) and (self.defibState == DEFIBState.Select):
            if (self.mi_pagevariables[DEFIB_SELECT] < 30) and (self.mi_pagevariables[DEFIB_SELECT]-5 >= 0):
                self.mi_pagevariables[DEFIB_SELECT] = self.mi_pagevariables[DEFIB_SELECT]-5
                self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_SELECT]} J SEL\nBIFASICO")
            elif self.mi_pagevariables[DEFIB_SELECT]-10 >= 0: # todo Agregar limite Superior
                self.mi_pagevariables[DEFIB_SELECT] = self.mi_pagevariables[DEFIB_SELECT]-10
                self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_SELECT]} J SEL\nBIFASICO")
            
            if self.mi_pagevariables[DEFIB_SELECT] != 0:
                self.ui.Charge_pushButton.setStyleSheet(PressedStylesheet)
            else: 
                self.ui.Charge_pushButton.setStyleSheet(Stylesheet)

    def onChargeButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.DEFIBPAGE) and (self.defibState == DEFIBState.Select) and (self.mi_pagevariables[DEFIB_SELECT] != 0):
            self.workingState = WorkingState.Busy
            self.defibState = DEFIBState.Charging
            # Asegurar disconnect y stop del timer
            if self.timer2.isActive():
                self.timer2.timeout.disconnect()
                self.timer2.stop()
            self.timer2.setInterval(600)
            self.timer2.timeout.connect(self.defibCharging)
            self.timer2.start()
            print("charge button was clicked")
    
    def defibCharging(self):
        print("first timer is working")
        if self.mi_pagevariables[DEFIB_CHARGE] != self.mi_pagevariables[DEFIB_SELECT]:
            if self.mi_pagevariables[DEFIB_CHARGE] < 10:
                self.mi_pagevariables[DEFIB_CHARGE] = self.mi_pagevariables[DEFIB_CHARGE]+1
            elif self.mi_pagevariables[DEFIB_CHARGE]>= 10 and self.mi_pagevariables[DEFIB_CHARGE]< 30:
                self.mi_pagevariables[DEFIB_CHARGE] = self.mi_pagevariables[DEFIB_CHARGE]+5
            else:
                self.mi_pagevariables[DEFIB_CHARGE] = self.mi_pagevariables[DEFIB_CHARGE]+10
            self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_CHARGE]} J CHG\nBIFASICO")
        else:
            self.defibState = DEFIBState.Charged
            self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_CHARGE]} J READY\nBIFASICO")
            self.timer2.stop()
            self.timer2.timeout.disconnect(self.defibCharging)
            self.ui.Charge_pushButton.setStyleSheet(Stylesheet)
            self.ui.Shock_pushButton.setStyleSheet(PressedStylesheet)
            print("first timer is stoped")

    def onDischargeButtonClicked(self):
        if(self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.DEFIBPAGE) and (self.defibState == DEFIBState.Charged):
            self.workingState = WorkingState.Busy
            # Asegurar disconnect y stop del timer
            if self.timer2.isActive():
                self.timer2.timeout.disconnect()
                self.timer2.stop()
            self.ui.DISCHARGE_pushButton.setStyleSheet(PressedStylesheet)
            self.ui.Shock_pushButton.setStyleSheet(Stylesheet)
            # Inicializar descarga
            self.timer2.setInterval(600)
            self.timer2.timeout.connect(self.defibDischarge)
            self.timer2.start()
            print("start of second timer ")

    def defibDischarge(self):
        print("second timer is working")
        if self.mi_pagevariables[DEFIB_CHARGE] != 0:
            if self.mi_pagevariables[DEFIB_CHARGE] < 10:
                self.mi_pagevariables[DEFIB_CHARGE] = self.mi_pagevariables[DEFIB_CHARGE]-1
            elif self.mi_pagevariables[DEFIB_CHARGE]>= 10 and self.mi_pagevariables[DEFIB_CHARGE]< 30:
                self.mi_pagevariables[DEFIB_CHARGE] = self.mi_pagevariables[DEFIB_CHARGE]-5
            else:
                self.mi_pagevariables[DEFIB_CHARGE] = self.mi_pagevariables[DEFIB_CHARGE]-10
            self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_CHARGE]} J DIS\nBIFASICO")
        else:
            self.defibState = DEFIBState.Select
            self.workingState = WorkingState.Idle
            self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_SELECT]} J SEL\nBIFASICO")
            self.ui.Charge_pushButton.setStyleSheet(PressedStylesheet)
            self.ui.Shock_pushButton.setStyleSheet(Stylesheet)
            self.timer2.stop()
            self.timer2.timeout.disconnect(self.defibDischarge)
            self.ui.DISCHARGE_pushButton.setStyleSheet(Stylesheet)
            
            print(" second timer is stoped")

    
    def onShockButtonClicked(self):
        if(self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.DEFIBPAGE) and (self.defibState == DEFIBState.Charged):
            self.defibState = DEFIBState.Shock
            self.workingState = WorkingState.Busy
            self.ui.Shock_pushButton.setStyleSheet(Stylesheet)
            if self.timer2.isActive():
                self.timer2.timeout.disconnect()
                self.timer2.stop()
            # Inicializar descarga
            self.timer2.setInterval(600)
            self.timer2.timeout.connect(self.defibShock)
            self.timer2.start()
            
    def defibShock(self):
        if (self.defibState == DEFIBState.Shock):
            self.defibState = DEFIBState.Select
            self.workingState = WorkingState.Idle
            self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_CHARGE]} J SHK\nBIFASICO")
        else:
            self.ui.defibLabel_pushButton.setText(f"DEFIB {self.mi_pagevariables[DEFIB_SELECT]} J SEL\nBIFASICO")
            self.ui.Charge_pushButton.setStyleSheet(PressedStylesheet)
            self.timer2.stop()
            self.timer2.timeout.disconnect(self.defibShock)  

    def resetPacerPage(self):
        self.mi_pagevariables = {PACEMAKER_MA:18, PACEMAKER_PPM:70,DEFIB_SELECT:0,DEFIB_CHARGE:0}
        self.ui.pacerValuemA_Label.setText(f"{self.mi_pagevariables[PACEMAKER_MA]} mA")
        self.ui.pacerValueppm_Label.setText(f"{self.mi_pagevariables[PACEMAKER_PPM]} ppm")
        self.ui.pacerLabel_pushButton.setStyleSheet(Stylesheet)

    def onPacerButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState != PageState.PACERPAGE) and (self.workingState != WorkingState.Busy):
            self.pageState = PageState.PACERPAGE
            self.ui.stackedWidget.setCurrentIndex(PageState.PACERPAGE)
            self.ui.plt.removeItem(self.data_line_channel1)
            self.ui.pacerLabel_pushButton.setStyleSheet(PressedStylesheet)
            self.resetDefib()
            self.resetCPRPage()
            print(PageState.PACERPAGE)
        elif (self.pageState != PageState.OFFPAGE) and (self.workingState != WorkingState.Busy):
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)
            self.pageState = PageState.DEFAULTPAGE
            # reset page variables
            self.resetPacerPage()
            self.data_line_channel1 = self.ui.plt.plot(self.x,self.channel1, pen = (162,249,161))
        
    
    def onPacerOutputUpButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.PACERPAGE):
            self.mi_pagevariables[PACEMAKER_MA] = self.mi_pagevariables[PACEMAKER_MA]+1
            self.ui.pacerValuemA_Label.setText(f"{self.mi_pagevariables[PACEMAKER_MA]} mA")
        
    def onPacerOutputDownButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.PACERPAGE) and (self.mi_pagevariables[PACEMAKER_MA]-1 >= 0):
            self.mi_pagevariables[PACEMAKER_MA] = self.mi_pagevariables[PACEMAKER_MA]-1
            self.ui.pacerValuemA_Label.setText(f"{self.mi_pagevariables[PACEMAKER_MA]} mA")

    def onPacerRateUpButtonCliked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.PACERPAGE):
            self.mi_pagevariables[PACEMAKER_PPM] = self.mi_pagevariables[PACEMAKER_PPM]+5
            self.ui.pacerValueppm_Label.setText(f"{self.mi_pagevariables[PACEMAKER_PPM]} ppm")
    
    def onPacerRateDownButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState==PageState.PACERPAGE) and (self.mi_pagevariables[PACEMAKER_PPM]-5 >= 0):
            self.mi_pagevariables[PACEMAKER_PPM] = self.mi_pagevariables[PACEMAKER_PPM]-5
            self.ui.pacerValueppm_Label.setText(f"{self.mi_pagevariables[PACEMAKER_PPM]} ppm")

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
            # Actualizacion de BP
            self.bp.HR = HEART_RATE

        elif(id == TEMPERATURE):
            self.ui.tempValue_Label.setText(str(data))
        elif(id == SPO):
            self.ui.SpO2Value_Label.setText(str(data))
            # Actualizacion de Spo2
            self.spo.spo2sl_change(self.mi_diccionario[SPO])
            self.spo.init_timer()
        elif(id == SYSPRESSURE):
            self.ui.pressureValue_Label.setText(str(data))
            # Actualizacion de Blood Pressure
            self.bp.P_in = self.mi_diccionario[SYSPRESSURE]
        elif(id == DIAPRESSURE):
            self.ui.pressureValue_Label.setText(str(data))
        elif(id == FR):
            self.ui.FRValue_Label.setText(str(data))
        elif(id == CO):
            self.ui.CO2Value_Label.setText(str(data))
            # Actualizacion de CO2
            #self.co2.loc = self.mi_diccionario[CO]
            #self.co2.init_timer()
        elif (id == SCENARIO):
            if (data == ScenarioState.Idle):
                self.scenarioState = ScenarioState.Idle
            elif (data == ScenarioState.ParoCardiaco):
                self.scenarioState =ScenarioState.ParoCardiaco
            elif (data == ScenarioState.TaquicardiaSinusal):
                self.scenarioState = ScenarioState.TaquicardiaSinusal
            elif (data == ScenarioState.BradicardiaSinusal):
                self.scenarioState = ScenarioState.BradicardiaSinusal
            elif (data == ScenarioState.FlutterAuricular):
                self.scenarioState = ScenarioState.FlutterAuricular
            elif (data == ScenarioState.FibrilacionAuricular):
                self.scenarioState = ScenarioState.FibrilacionAuricular
            elif (data == ScenarioState.TaquicardiaAuricular):
                self.scenarioState = ScenarioState.TaquicardiaAuricular
            elif (data == ScenarioState.ArritmiaSinusal):
                self.scenarioState = ScenarioState.ArritmiaSinusal
            elif (data == ScenarioState.FibrilacionVentricular):
                self.scenarioState.FibrilacionVentricular
            elif (data == ScenarioState.TaquicardiaVentricular):
                self.scenarioState = ScenarioState.TaquicardiaVentricular
            elif (data == ScenarioState.Asistolia):
                self.scenarioState = ScenarioState.Asistolia


        else:
            print("Invalid ID")

    def testWorker(self, id, data):
        # Cambiar diccionario
        s_id = str(id)
        self.mi_diccionario[s_id] = data
        print(self.mi_diccionario)
        self.updateUI(s_id, data)

    ##########################################################################################
    # Funciones de esenarios     
    def scenExperiment(self):
        self.scenarioState = ScenarioState.ParoCardiaco
        print("ParoCardiaco")
    def scenDefalt(self):
        self.scenarioState = ScenarioState.Idle
        


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

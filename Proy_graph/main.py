### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg 
import sys 
import numpy as np
from data_test import ecg_signal, obtainSignals, Atrialflutter, Sinusarrhythmia, Atrialfibrillation, VTHR, VF, SBR
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
from connection import addPorts, generate_crc32_table, onScanReturnButtonClicked, onConnectConfirmButtonClicked
from constants import SignalState, DEFIBState, WorkingState, ScenarioState, PageState, HEART_RATE, TEMPERATURE,SPO, SYSPRESSURE, DIAPRESSURE, FR, CO, SCENARIO,PACEMAKER_MA, PACEMAKER_PPM, DEFIB_SELECT, DEFIB_CHARGE, NUM_CHANNELS, CHANNEL_OFFSETS, CHANNEL_TEXT_POSITIONS

import spo
import co2
import bp

from time import time
from timeit import default_timer as timerX


# Manejo de arreglos en la senal 
# todo, cambiar el manejo de datos con collections deque


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
        self.mi_diccionario = {HEART_RATE:60,TEMPERATURE:0,SPO:0,SYSPRESSURE:0,DIAPRESSURE:0,FR:0, CO:0}
        self.mi_pagevariables = {PACEMAKER_MA:18, PACEMAKER_PPM:70,DEFIB_SELECT:0,DEFIB_CHARGE:0}
        self.generateSig = 0
        self.ecg12 = 0
        self.parserState = ParserState.Type
        self.spo = spo.SPO()
        self.co2 = co2.CO2()
        self.bp =bp.BloodPressure()

        self.timestamp = 0.0

        self.generateSig = obtainSignals()
        self.ecg12 = self.generateSig.generateSignals(self.mi_diccionario[HEART_RATE])
        self.rsp = list(self.generateSig.generate_rsp())

        self.data = []
        self.channels = [] #data to graph
        self.data_lines = [] #plot data
        self.text_items = []
        self.signalIndex = 0
        
        # Manejo de tiempos
            # Timers 
        self.timer = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.time = QtCore.QTime()
        self.elapsedTime = QtCore.QElapsedTimer()

        self.start = timerX()


        # Connections
        self.s = ""
        self.sCoder = SerialCoder()
        self.worker = WorkerThread(self.s, self.sCoder)
        self.sPorts = list(portList.comports())
        addPorts(self.ui, self.sPorts)
        self.sConnected = False
        self.custom_crc_table = {}
        self.poly = 0x04C11DB7
        generate_crc32_table(self.poly, self.custom_crc_table)


        #Button Control
        self.ui.DEA_pushButton.pressed.connect(self.displayHello)
        self.ui.SYNC_pushButton.pressed.connect(self.displayHello)
        # Confirm es connect y return es scan 
        self.ui.confirmMenu_pushButton.pressed.connect(lambda: onConnectConfirmButtonClicked(self.ui, self.ui.port_comboBox, self.s, self.worker, self.sCoder))
        self.ui.returnMenu_pushButton.pressed.connect(lambda: onScanReturnButtonClicked(self.ui, self.sPorts))

        self.ui.alarmMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.CPRMenu_pushButton.pressed.connect(self.onCPRButtonClicked)
        self.ui.sizeMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.LEADMenu_pushButton.pressed.connect(self.onLeadMenuButtonClicked)
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

        channel_configs = [
                            {'label': 'II', 'color': (162,249,161), 'pos': (130, -0.2), 'fillLevel': None},
                            {'label': 'Pleth', 'color': (134,234,233), 'pos': (110, -0.3), 'fillLevel': None},
                            {'label': 'ABP', 'color': (136,51,64), 'pos': (90, -0.3), 'fillLevel': None},
                            {'label': 'Resp', 'color': (255,222,89), 'pos': (70, -0.3), 'fillLevel': None},
                            {'label': 'CO2', 'color': (171,171,171), 'pos': (50, -0.3), 'fillLevel': -0.3},
                            {'label': 'avF', 'color': (171,171,171), 'pos': (50, -0.3), 'fillLevel': None},
                            # Add or remove channel configs as needed
                        ]

        # Plot configuration
        #self.ui.plt.getPlotItem().hideAxis('left')
        self.ui.plt.setYRange(0, 5.5)

        # #Eje en x 
        # self.x = deque(np.linspace(0,4,self.graphlength),maxlen=self.graphlength)
        self.x = deque([], maxlen=self.graphlength)

        for i, config in enumerate(channel_configs):
            y_offset = config['pos'][0]
            # Create the deque with initial values
            #channel_deque = deque([y_offset for _ in range(self.graphlength)], maxlen=self.graphlength)
            channel_deque = deque([], maxlen=self.graphlength)
            self.channels.append(channel_deque)

        #     # Create the plot line with an optional fillLevel
            if config.get('fillLevel') is not None:
                brush = pg.mkBrush(config['color'] + (60,))
                data_line = self.ui.plt.plot(self.x, channel_deque, pen=config['color'], fillLevel=config['fillLevel'], brush=brush)
            else:
                data_line = self.ui.plt.plot(self.x, channel_deque, pen=config['color'])
            self.data_lines.append(data_line)

        #     # Create the label text
        #     text_item = pg.TextItem(config['label'], color=config['color'])
        #     text_item.setPos(config['pos'][1], y_offset)
        #     self.ui.plt.addItem(text_item)
        #     self.text_items.append(text_item)
        
    def signalScenarioData(self):
       
        if self.scenarioState == ScenarioState.Idle:
            channel_sources = [
            self.ecg12['II']*10,
            self.spo.sR,
            self.bp.data,
            self.rsp,
            self.co2.data,
            self.ecg12["aVF"]
            ]
            self.data = [list(source) if not isinstance(source, list) else source for source in channel_sources]
            
        elif self.scenarioState == ScenarioState.ParoCardiaco:
            self.dataChannel1 = ([0]*self.graphlength)
            self.dataChannel2 = (list(self.spo.sR))
            self.dataChannel3 = ([0]*self.graphlength)
            self.dataChannel4 = (self.rsp)
            self.dataChannel5 = list(self.co2.data)
            self.dataChannel6 = (self.ecg12["aVF"])
        # elif self.scenarioState == ScenarioState.TaquicardiaSinusal:
        #     print(ScenarioState.TaquicardiaSinusal)
        elif self.scenarioState == ScenarioState.BradicardiaSinusal:
            self.dataChannel1 = list(pd.DataFrame(SBR)[0]*10)
            #print(ScenarioState.BradicardiaSinusal)
        elif self.scenarioState == ScenarioState.FlutterAuricular:
            self.dataChannel1 = list(pd.DataFrame(Atrialflutter)[0]*10)
            #print(ScenarioState.FlutterAuricular)
        elif self.scenarioState == ScenarioState.FibrilacionAuricular:
            self.dataChannel1 = list(pd.DataFrame(Atrialfibrillation)[0]*10)
            #print(ScenarioState.FibrilacionAuricular)
        # elif self.scenarioState == ScenarioState.TaquicardiaAuricular:
        #     print(ScenarioState.TaquicardiaAuricular)
        # elif self.scenarioState == ScenarioState.ArritmiaSinusal:
        #     self.dataChannel1 = list(pd.DataFrame(Sinusarrhythmia)[0]*10)
        #     print(ScenarioState.ArritmiaSinusal)
        # elif self.scenarioState == ScenarioState.FibrilacionVentricular:
        #     self.dataChannel1 = list(pd.DataFrame(VF)[0]*10)
        #     print(ScenarioState.FibrilacionVentricular)
        # elif self.scenarioState == ScenarioState.TaquicardiaVentricular:
        #     self.dataChannel1 = list(pd.DataFrame(VTHR)[0]*10)
        #     print(ScenarioState.TaquicardiaVentricular)
        # elif self.scenarioState == ScenarioState.Asistolia:
        #     print(ScenarioState.Asistolia)
            

    def Update_Grahp(self):
        self.tPPG = time() - self.timestamp
        self.spo.update(self.mi_diccionario[HEART_RATE], self.tPPG)
        self.bp.update_plot(self.mi_diccionario[HEART_RATE], self.tPPG)
        self.co2.update_plot(self.mi_diccionario[FR], self.tPPG)
        # Initialize data channels with zeros if not in the correct page state
        #if  self.pageState != PageState.LEADPAGE1 and self.pageState != PageState.LEADPAGE2:
            #self.signalScenarioData()
        # else:
        #     self.dataChannel1 = (self.ecg12[self.leadConfig["text1"]]*10)
        #     self.dataChannel2 = (self.ecg12[self.leadConfig["text2"]]*10)
        #     self.dataChannel3 = (self.ecg12[self.leadConfig["text3"]]*10)
        #     self.dataChannel4 = (self.ecg12[self.leadConfig["text4"]]*10)
        #     self.dataChannel5 = (self.ecg12[self.leadConfig["text5"]]*10)
        #     self.dataChannel6 = (self.ecg12[self.leadConfig["text6"]]*10)

        if(self.signalIndex >= (self.graphlength)-1):
            self.signalIndex = 0

        self.signalIndex = self.signalIndex + 1

        # for i in range (NUM_CHANNELS):
        #     self.channels[i].append(self.data[i][self.signalIndex] + CHANNEL_OFFSETS[i])
        #     # Update the position of each channel's text label
        #     self.text_items[i].setPos(self.x[0] - 0.2, CHANNEL_OFFSETS[i])
        #     # Update the data line for each channel with the new data
        #     self.data_lines[i].setData(self.x, self.channels[i])

        
        
        self.channels[0].append(self.ecg12['II'][self.signalIndex] + CHANNEL_OFFSETS[1])
        self.channels[1].append(self.spo.sR + CHANNEL_OFFSETS[2])
        self.channels[2].append(self.bp.p + CHANNEL_OFFSETS[3])
        self.channels[3].append(self.rsp[self.signalIndex] + CHANNEL_OFFSETS[4])
        self.channels[4].append(self.co2.co+ CHANNEL_OFFSETS[5])
        self.x.append(self.tPPG)
        self.data_lines[0].setData(x=list(self.x)[1:], y = list(self.channels[0])[1:])
        self.data_lines[1].setData(x=list(self.x)[1:], y = list(self.channels[1])[1:])
        self.data_lines[2].setData(x=list(self.x)[1:], y = list(self.channels[2])[1:])
        self.data_lines[3].setData(x=list(self.x)[1:], y = list(self.channels[3])[1:])
        self.data_lines[4].setData(x=list(self.x)[1:], y = list(self.channels[4])[1:])
        #self.ui.plt.clear()
        #self.ui.plt.plot(x=list(self.x)[1:], y = list(self.channels[1])[1:])


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
        self.timestamp = time()
        if (self.pageState != PageState.OFFPAGE):
            if(self.signalState == SignalState.Idle):
                self.setDefaultValues()
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
                       self.ui.plt.removeItem(self.data_line_channel4)
                
                self.signalState = SignalState.Playing
                # Envio de estado por serial 
                if self.state != State.IdleDisconnected:
                    self.worker.encodeMesage(8,1)
                    self.worker.sendMessage()
                
                # Manejo de timer y time
                self.elapsedTime.start()
                self.timer.setInterval(2)
                self.timer.timeout.connect(self.Update_Grahp)
                #self.timer.timeout.connect(self.Update_Time)
                self.timer.start()

    def onPauseButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.signalState == SignalState.Playing) :
            self.timer.stop()
            self.signalState = SignalState.Pause
            # Envio de estado por serial 
            if self.state != State.IdleDisconnected:
                self.worker.encodeMesage(8,2)
                self.worker.sendMessage()
        
    def onStopButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.signalState != SignalState.Idle):
            self.timer.stop()
            self.setDefaultValues()
            self.ui.plt.clear()
            self.signalIndex = 0

            self.signalState = SignalState.Stop

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
        self.signalIndex = 0
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
            self.ui.plt.removeItem(self.data_line_channel4)
            print(PageState.CPRPAGE)
        elif (self.pageState != PageState.OFFPAGE) and (self.workingState != WorkingState.Busy):
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)
            self.pageState = PageState.DEFAULTPAGE
            self.resetCPRPage()
            self.data_line_channel4 = self.ui.plt.plot(self.x,self.channel4, pen = (255,222,89))
    
    def onDEFIBButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE) and (self.pageState != PageState.DEFIBPAGE) and (self.workingState != WorkingState.Busy):
            self.pageState = PageState.DEFIBPAGE
            self.defibState = DEFIBState.Select
            self.ui.plt.removeItem(self.data_line_channel4)
            self.resetPacerPage()
            self.resetCPRPage()
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
            self.data_line_channel4 = self.ui.plt.plot(self.x,self.channel4, pen = (255,222,89))
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
            self.ui.plt.removeItem(self.data_line_channel4)
            self.ui.pacerLabel_pushButton.setStyleSheet(PressedStylesheet)
            self.resetDefib()
            self.resetCPRPage()
            print(PageState.PACERPAGE)
        elif (self.pageState != PageState.OFFPAGE) and (self.workingState != WorkingState.Busy):
            self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)
            self.pageState = PageState.DEFAULTPAGE
            # reset page variables
            self.resetPacerPage()
            self.data_line_channel4 = self.ui.plt.plot(self.x,self.channel4, pen = (255,222,89))
          
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

    def onLeadMenuButtonClicked(self):
        if (self.pageState != PageState.OFFPAGE)  and (self.signalState == SignalState.Playing) and (self.pageState in [PageState.DEFAULTPAGE, PageState.LEADPAGE1, PageState.LEADPAGE2]):
            if self.pageState != PageState.LEADPAGE1 and self.pageState != PageState.LEADPAGE2:
                self.pageState = PageState.LEADPAGE1
                self.workingState = WorkingState.Busy
                self.ui.stackedWidget.setCurrentIndex(PageState.DEFAULTPAGE)
                self.resetDefib()
                self.resetCPRPage()
                self.resetPacerPage()
                self.ui.plt.setYRange(20, 140)
                self.ui.plt.addItem(self.channel6Text)
                self.leadConfig = {"text1":"I", "text2":"II","text3":"III","text4":"aVL","text5":"aVR", "text6":"aVF","ch1":(162,249,161),"ch2":(162,249,161),"ch3":(162,249,161), "ch4":(162,249,161),"ch5":(162,249,161),"ch6":(162,249,161)}
                self.ui.plt.addItem(self.data_line_channel6)
                self.data_line_channel5.setBrush(171,171,171, 0)
                
                startChannel1 = [130]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text1"]]*10)+130)[:2000]
                startChannel2 = [110]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text2"]]*10)+110)[:2000]
                startChannel3 = [90]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text3"]]*10)+90)[:2000]
                startChannel4 = [70]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text4"]]*10)+70)[:2000]
                startChannel5 = [50]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text5"]]*10)+50)[:2000]
                startChannel6 = [30]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text6"]]*10)+30)[:2000]
                
                self.channel1 = deque(startChannel1 + list((self.ecg12[self.leadConfig["text1"]]*10)+130)[:self.signalIndex],maxlen = 2000)
                self.channel2 = deque(startChannel2 + list((self.ecg12[self.leadConfig["text2"]]*10)+110)[:self.signalIndex],maxlen = 2000)
                self.channel3 = deque(startChannel3 + list((self.ecg12[self.leadConfig["text3"]]*10)+90)[:self.signalIndex],maxlen = 2000)
                self.channel4 = deque(startChannel4 + list((self.ecg12[self.leadConfig["text4"]]*10)+70)[:self.signalIndex],maxlen = 2000)
                self.channel5 = deque(startChannel5 + list((self.ecg12[self.leadConfig["text5"]]*10)+50)[:self.signalIndex],maxlen = 2000)
                self.channel6 = deque(startChannel6 + list((self.ecg12[self.leadConfig["text6"]]*10)+30)[:self.signalIndex],maxlen = 2000)
            elif self.pageState == PageState.LEADPAGE1:
                self.pageState = PageState.LEADPAGE2
                
                self.leadConfig = {"text1":"V1", "text2":"V2","text3":"V3","text4":"V4","text5":"V5", "text6":"V6","ch1":(162,249,161),"ch2":(162,249,161),"ch3":(162,249,161), "ch4":(162,249,161),"ch5":(162,249,161),"ch6":(162,249,161)}
                startChannel1 = [130]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text1"]]*10)+130)[:2000]
                startChannel2 = [110]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text2"]]*10)+110)[:2000]
                startChannel3 = [90]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text3"]]*10)+90)[:2000]
                startChannel4 = [70]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text4"]]*10)+70)[:2000]
                startChannel5 = [50]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text5"]]*10)+50)[:2000]
                startChannel6 = [30]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text6"]]*10)+30)[:2000]
            
                self.channel1 = deque(startChannel1 + list((self.ecg12[self.leadConfig["text1"]]*10)+130)[:self.signalIndex],maxlen = 2000)
                self.channel2 = deque(startChannel2 + list((self.ecg12[self.leadConfig["text2"]]*10)+110)[:self.signalIndex],maxlen = 2000)
                self.channel3 = deque(startChannel3 + list((self.ecg12[self.leadConfig["text3"]]*10)+90)[:self.signalIndex],maxlen = 2000)
                self.channel4 = deque(startChannel4 + list((self.ecg12[self.leadConfig["text4"]]*10)+70)[:self.signalIndex],maxlen = 2000)
                self.channel5 = deque(startChannel5 + list((self.ecg12[self.leadConfig["text5"]]*10)+50)[:self.signalIndex],maxlen = 2000)
                self.channel6 = deque(startChannel6 + list((self.ecg12[self.leadConfig["text6"]]*10)+30)[:self.signalIndex],maxlen = 2000)
            elif self.pageState == PageState.LEADPAGE2:
                self.data_line_channel5.setBrush(171,171,171, 60)
                self.pageState = PageState.DEFAULTPAGE
                self.workingState = WorkingState.Idle
                self.leadConfig = {"text1":"II", "text2":"Pleth","text3":"ABP","text4":"Resp","text5":"CO2", "text6":"aVF","ch1":(162,249,161),"ch2":(134,234,233),"ch3":(136,51,64), "ch4":(255,222,89),"ch5":(171,171,171),"ch6":(162,249,161)}
                self.ui.plt.removeItem(self.data_line_channel6)
                self.ui.plt.removeItem(self.channel6Text)
                self.ui.plt.setYRange(40, 140)

                startChannel1 = [130]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text1"]]*10)+130)[:2000]
                startChannel2 = [110]*2000 if self.adderFlag == 0 else list(pd.DataFrame(list(self.spo.dataIR))[0]+110)[:2000]
                startChannel3 = [90]*2000 if self.adderFlag == 0 else list(pd.DataFrame(list(self.bp.data))[0]+90)[:2000]
                startChannel4 = [70]*2000 if self.adderFlag == 0 else list(pd.DataFrame(list(self.rsp))[0]+70)[:2000]
                startChannel5 = [50]*2000 if self.adderFlag == 0 else list(pd.DataFrame(list(self.co2.data))[0]+50)[:2000]
                startChannel6 = [30]*2000 if self.adderFlag == 0 else list((self.ecg12[self.leadConfig["text6"]]*10)+30)[:2000]
                
                self.channel1 = deque(startChannel1 + list((self.ecg12[self.leadConfig["text1"]]*10)+130)[:self.signalIndex],maxlen = 2000)
                self.channel2 = deque(startChannel2 + list(pd.DataFrame(list(self.spo.dataIR))[0]+110)[:self.signalIndex],maxlen = 2000)
                self.channel3 = deque(startChannel3 + list(pd.DataFrame(list(self.bp.data))[0]+90)[:self.signalIndex],maxlen = 2000)
                self.channel4 = deque(startChannel4 + list(pd.DataFrame(list(self.rsp))[0]*10+70)[:self.signalIndex],maxlen = 2000)
                self.channel5 = deque(startChannel5 + list(pd.DataFrame(list(self.co2.data))[0]+50)[:self.signalIndex],maxlen = 2000)
                self.channel6 = deque(startChannel6 + list((self.ecg12[self.leadConfig["text6"]]*10)+30)[:self.signalIndex],maxlen = 2000)
                
            self.channel1Text.setText(self.leadConfig["text1"])
            self.channel2Text.setText(self.leadConfig["text2"])
            self.channel3Text.setText(self.leadConfig["text3"])
            self.channel4Text.setText(self.leadConfig["text4"])
            self.channel5Text.setText(self.leadConfig["text5"])
            self.channel6Text.setText(self.leadConfig["text6"])

            self.channel1Text.setColor(self.leadConfig["ch1"])
            self.channel2Text.setColor(self.leadConfig["ch2"])
            self.channel3Text.setColor(self.leadConfig["ch3"])
            self.channel4Text.setColor(self.leadConfig["ch4"])
            self.channel5Text.setColor(self.leadConfig["ch5"])
            self.channel6Text.setColor(self.leadConfig["ch6"])

            self.data_line_channel1.setPen(self.leadConfig["ch1"])
            self.data_line_channel2.setPen(self.leadConfig["ch2"])
            self.data_line_channel3.setPen(self.leadConfig["ch3"])
            self.data_line_channel4.setPen(self.leadConfig["ch4"])
            self.data_line_channel5.setPen(self.leadConfig["ch5"])
            self.data_line_channel6.setPen(self.leadConfig["ch6"])

    ##########################################################################################
    # Funciones Para el manejo del tiempo  

    def Update_Time(self):
        self.updateElapsedTime()
        self.ui.simulationTimeValue_pushButton.setText(str(self.elapsed_time))
    
    def updateElapsedTime(self):
        self.elapsed_time = self.time.addMSecs(self.elapsedTime.elapsed()).toString("hh:mm:ss")

    def displayHello(self):
        print("hello")
    
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
        self.updateUI(s_id, data)

    ##########################################################################################
    # Funciones de esenarios     
    def scenExperiment(self):
        self.scenarioState = ScenarioState.ArritmiaSinusal
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

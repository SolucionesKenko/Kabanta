### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore
#import pyqtgraph as pg 
import sys 
import numpy as np
from data_test import ecg_signal, ecg12
from window import Ui_window
from Bluetooth_sample import DeviceFinder


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_window()
        self.ui.setupUi(self)
        self.bt = DeviceFinder()
        #self.bt.startDeviceDiscovery()
        


        #Button Control
        self.Ui_window = Ui_window()
        self.ui.DEFIB_pushButton.pressed.connect(self.displayHello)
        self.ui.Charge_pushButton.pressed.connect(self.displayHello)
        self.ui.Shock_pushButton.pressed.connect(self.displayHello)
        self.ui.DEA_pushButton.pressed.connect(self.displayHello)
        self.ui.SYNC_pushButton.pressed.connect(self.displayHello)
        self.ui.confirmMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.returnMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.alarmMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.CPRMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.sizeMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.LEADMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.DPO_pushButton.pressed.connect(self.displayHello)
        self.ui.DPR_pushButton.pressed.connect(self.displayHello)
        self.ui.UPO_pushButton.pressed.connect(self.displayHello)
        self.ui.UPR_pushButton.pressed.connect(self.displayHello)
        self.ui.config_pushButton.pressed.connect(self.Pokemon)
        self.ui.CPRMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.LEADMenu_pushButton.pressed.connect(self.displayHello)
        self.ui.UpEnergySelect_pushButton.pressed.connect(self.displayHello)
        self.ui.DownEnergySelect_pushButton.pressed.connect(self.displayHello)
        self.ui.play_RoundButton.pressed.connect(self.displayHello)
        self.ui.pause_RoundButton.pressed.connect(self.displayHello)
        self.ui.stop_RoundButton.pressed.connect(self.displayHello)
        self.ui.question_RoundButton.pressed.connect(self.displayHello)
        self.ui.OnOff_RoundButton.pressed.connect(self.displayHello)
        self.ui.UpRoundTriangle.pressed.connect(self.displayHello)
        self.ui.DownRoundTriangle.pressed.connect(self.displayHello)
    

        print(type(ecg12))
        ### Final de configuracion de los Widgets
        ### Codigo de main
        #Agregados al Layout vertical
        self.SignalGrahps()
        #Actualizacion de grafica
        self.su = 1
        self.timer = QtCore.QTimer()
        self.timer.setInterval(30)
        #self.timer.timeout.connect(self.Update_Grahp)
        self.timer.start()
        
        # User code starts Here 
    def Pokemon(self):
        print("inicio")
        print("final")

    ### Funciones Agregados  
    def SignalGrahps(self):
        #Eje en x 
        self.x = list(range(100))
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
    


    def Update_Grahp(self):
        self.su = self.su + 1
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        #self.ecgSignal = self.ecgSignal

        self.der1 = self.der1[1:]  # Remove the first
        self.der1.append(ecg12['I'][self.su*10])  # Add a new random value.
        

        self.der2 = self.der2[1:]  # Remove the first
        self.der2.append(ecg12['II'][self.su*10]-2)  # Add a new random value.

        self.der3 = self.der3[1:]  # Remove the first
        self.der3.append(ecg_signal[self.su][2]-4)  # Add a new random value.

        self.data_line_der1.setData(self.x, self.der1)  # Update the data.
        self.data_line_der2.setData(self.x, self.der2)
        self.data_line_der3.setData(self.x, self.der3)

    def displayHello(self):
        print("Hello")

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
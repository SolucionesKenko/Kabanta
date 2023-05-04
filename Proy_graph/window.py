### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg 
import sys 
import numpy as np
import os
from data_test import ecg_signal
Horiz_size = 800
Vert_size = 480 



class Ui_window(object):
    def setupUi(self, Form):
        ### Inicio de Configuracion de los Widgets
        Form.setObjectName("Pokemon")
        Form.resize(Horiz_size, Vert_size)
        #Widget de Layout vertical para graficas verticales Preconfiguracion
        self.Graph_verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.Graph_verticalLayoutWidget.setGeometry(QtCore.QRect(15, 50, 550, 350))
        self.Graph_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Graph_verticalLayout = QtWidgets.QVBoxLayout(self.Graph_verticalLayoutWidget)
        self.plt = pg.PlotWidget(title = 'Signo vital 1')
        #self.plt.showGrid(x=True, y=True)
        self.Graph_verticalLayout.addWidget(self.plt)
        ## todo Verificar que hace estos dos lineas
        #self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout.setObjectName("verticalLayout")

        self.DCS_verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.DCS_verticalLayoutWidget.setGeometry(QtCore.QRect(580, 50, 120, 150))
        self.DCS_verticalLayoutWidget.setObjectName("DCS_verticalLayoutWidget")
        self.DCS_verticalLayout = QtWidgets.QVBoxLayout(self.DCS_verticalLayoutWidget)
            #Push Button 
        self.DEFIB_pushButton = QtWidgets.QPushButton(self.DCS_verticalLayoutWidget)
        self.DEFIB_pushButton.setObjectName("DEFIB_pushButton")
        self.DCS_verticalLayout.addWidget(self.DEFIB_pushButton)
        self.Charge_pushButton = QtWidgets.QPushButton(self.DCS_verticalLayoutWidget)
        self.Charge_pushButton.setObjectName("Charge_pushButton")
        self.DCS_verticalLayout.addWidget(self.Charge_pushButton)
        self.Shock_pushButton = QtWidgets.QPushButton(self.DCS_verticalLayoutWidget)
        self.Shock_pushButton.setObjectName("Shock_pushButton")
        self.DEFIB_pushButton.setStyleSheet(Stylesheet)
        self.Charge_pushButton.setStyleSheet(Stylesheet)
        self.Shock_pushButton.setStyleSheet(Stylesheet)
        

        #self.Shock_pushButton.setback()
        self.DCS_verticalLayout.addWidget(self.Shock_pushButton)
        ## todo Verificar que hace estos dos lineas
        #self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout.setObjectName("verticalLayout")"""
        
        
        self.retranslateUi(Form)
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Piplup"))
        self.DEFIB_pushButton.setText(_translate('Form', '1 DEFIB'))
        self.Charge_pushButton.setText(_translate('Form','2 CHARGE '))
        self.Shock_pushButton.setText(_translate('Form','3 SHOCK'))

Stylesheet = """

#Charge_pushButton {
    color: black; 
    background-color: lightgray; 
    border-style: outset; 
    border-width: 1px; 
    border-radius: 8px; 
    border-color: beige; 
    padding: 5px; 
    font: bold 11px; 
    }

#DEFIB_pushButton {
    color: black; 
    background-color: lightgray; 
    border-style: outset; 
    border-width: 1px; 
    border-radius: 8px; 
    border-color: beige; 
    padding: 5px; 
    font: bold 11px; 
    }

#Shock_pushButton {
    color: black; 
    background-color: lightgray; 
    border-style: outset; 
    border-width: 1px; 
    border-radius: 8px; 
    border-color: beige; 
    padding: 5px; 
    font: bold 11px; 
    }

"""
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    Form = QtWidgets.QWidget()
    ui = Ui_window()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
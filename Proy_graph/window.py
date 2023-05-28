### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg 
import sys 
from StylesheetFormat import Stylesheet
import pantalla_config
from samples import RoundButton



class Ui_window(object):
    def setupUi(self, Form):
        ### Inicio de Configuracion de los Widgets
        Form.setObjectName("Pokemon")
        Form.resize(pantalla_config.Horiz_size, pantalla_config.Vert_size)
        #Widget de Layout vertical para la graficacion de senales 
        self.Graph_verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.Graph_verticalLayoutWidget.setGeometry(QtCore.QRect(pantalla_config.grah_CoordX1,
                                                                pantalla_config.grah_CoordY1, 
                                                                pantalla_config.grah_HorizSize, 
                                                                pantalla_config.grah_VertSize))
        self.Graph_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Graph_verticalLayout = QtWidgets.QVBoxLayout(self.Graph_verticalLayoutWidget)
        self.plt = pg.PlotWidget()
        #self.plt.showGrid(x=True, y=True)
        self.Graph_verticalLayout.addWidget(self.plt)

        ### Widget Layout vertical para botones Defib, Charge, Shock
        self.DCS_verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.DCS_verticalLayoutWidget.setGeometry(QtCore.QRect(pantalla_config.DCS_CoordX1,
                                                                pantalla_config.DCS_CoordY1,
                                                                pantalla_config.DCS_HorizSize,
                                                                pantalla_config.DCS_VertSize))
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
        self.DCS_verticalLayout.addWidget(self.Shock_pushButton)
            #StyleSheet Button
        self.DEFIB_pushButton.setStyleSheet(Stylesheet)
        self.Charge_pushButton.setStyleSheet(Stylesheet)
        self.Shock_pushButton.setStyleSheet(Stylesheet)
        
        ### Widget Layout Horizontal Play, Pause, Stop, Question
        self.PPSQ_HorizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.PPSQ_HorizontalLayoutWidget.setGeometry(QtCore.QRect(pantalla_config.PPSQ_CoordX1,
                                                                pantalla_config.PPSQ_CoordY1, 
                                                                pantalla_config.PPSQ_HorizSize, 
                                                                pantalla_config.PPSQ_VertSize))
        self.PPSQ_HorizontalLayoutWidget.setObjectName("PPSQ_HorizontalLayoutWidget")
        self.PPSQ_HorizontalLayout = QtWidgets.QHBoxLayout(self.PPSQ_HorizontalLayoutWidget)
        #self.PPSQ_HorizontalLayout.setContentsMargins
            #Button
        self.play_RoundButton = RoundButton()
        self.play_RoundButton.setObjectName("play_RoundButton")
        self.PPSQ_HorizontalLayout.addWidget(self.play_RoundButton)
        self.pause_RoundButton = RoundButton()
        self.pause_RoundButton.setObjectName("pause_RoundButton")
        self.PPSQ_HorizontalLayout.addWidget(self.pause_RoundButton)
        self.stop_RoundButton = RoundButton()
        self.stop_RoundButton.setObjectName("stop_RoundButton")
        self.PPSQ_HorizontalLayout.addWidget(self.stop_RoundButton)
        self.question_RoundButton = RoundButton()
        self.question_RoundButton.setObjectName("question_RoundButton")
        self.PPSQ_HorizontalLayout.addWidget(self.question_RoundButton)
        self.OnOff_RoundButton = RoundButton()
        self.OnOff_RoundButton.setObjectName("OnOff_RoundButton")
        self.PPSQ_HorizontalLayout.addWidget(self.question_RoundButton)
            #StyleSheet

        ### Energy Select, Dea and Sync Buttons
            # Up Energey Select (UES)
        self.UpEnergySelect_pushButton = QtWidgets.QPushButton(Form)
        self.UpEnergySelect_pushButton.setGeometry(QtCore.QRect(pantalla_config.UES_CoordX1,
                                                                pantalla_config.UES_CoordY1,
                                                                pantalla_config.UES_HorizSize,
                                                                pantalla_config.UES_VertSize))
        self.UpEnergySelect_pushButton.setObjectName("UpEnergySelect_pushButton")
        self.UpEnergySelect_pushButton.setStyleSheet(Stylesheet)
            # Down Energey Select (DES)
        self.DownEnergySelect_pushButton = QtWidgets.QPushButton(Form)
        self.DownEnergySelect_pushButton.setGeometry(QtCore.QRect(pantalla_config.DES_CoordX1,
                                                                pantalla_config.DES_CoordY1,
                                                                pantalla_config.DES_HorizSize,
                                                                pantalla_config.DES_VertSize))
        self.DownEnergySelect_pushButton.setObjectName("DownEnergySelect_pushButton")
        self.DownEnergySelect_pushButton.setStyleSheet(Stylesheet)
            # DEA
        self.DEA_pushButton = QtWidgets.QPushButton(Form)
        self.DEA_pushButton.setGeometry(QtCore.QRect(pantalla_config.DEA_CoordX1,
                                                    pantalla_config.DEA_CoordY1,
                                                    pantalla_config.DEA_HorizSize,
                                                    pantalla_config.DEA_VertSize))
        self.DEA_pushButton.setObjectName("DEA_pushButton")
        self.DEA_pushButton.setStyleSheet(Stylesheet)
            #SYNC
        self.SYNC_pushButton = QtWidgets.QPushButton(Form)
        self.SYNC_pushButton.setGeometry(QtCore.QRect(pantalla_config.SYNC_CoordX1,
                                                    pantalla_config.SYNC_CoordY1,
                                                    pantalla_config.SYNC_HorizSize,
                                                    pantalla_config.SYNC_VertSize))
        self.SYNC_pushButton.setObjectName("SYNC_pushButton")
        self.SYNC_pushButton.setStyleSheet(Stylesheet)
        
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


        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    Form = QtWidgets.QWidget()
    ui = Ui_window()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
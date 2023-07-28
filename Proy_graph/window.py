### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg 
import sys 
from StylesheetFormat import Stylesheet
import pantalla_config
from samples import UPRoundTriangle, DOWNRoundTriangle




class Ui_window(object):
    def setupUi(self, Form):
        ### Inicio de Configuracion de los Widgets
        Form.setObjectName("Pokemon")
        Form.resize(pantalla_config.Horiz_size, pantalla_config.Vert_size)

        ### Round Rectangle for Plotting Graph
        self.roundRectGraph_Qpaint = QtWidgets.QLabel(Form)
        self.roundRectGraph_Qpaint.setGeometry(QtCore.QRect(pantalla_config.roundRectGrah_CoordX1 -3,
                                            pantalla_config.roundRectGrah_CoordY1-3,
                                            pantalla_config.roundRectGrah_HorizSize+6,
                                            pantalla_config.roundRectGrah_VertSize+6))
        self.roundRectGraph_Qpaint.setObjectName("roundRectGraph_Qpaint")
        self.canvasLabel = QtGui.QPixmap(pantalla_config.roundRectGrah_HorizSize+6,pantalla_config.roundRectGrah_VertSize+6)
        self.canvasLabel.fill(QtGui.QColor(209,209,209))
        self.roundRectGraph_Qpaint.setPixmap(self.canvasLabel)
        painter = QtGui.QPainter(self.roundRectGraph_Qpaint.pixmap())
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(0,0,0))
        brush.setStyle(1)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(34,34,34))
        painter.setPen(pen)
        painter.drawRoundedRect(3, 3,pantalla_config.roundRectGrah_HorizSize, pantalla_config.roundRectGrah_VertSize, 30, 30)
        painter.end()

        ### Round Rectangle for the DEFIB Charge and Shock button/Area
        self.roundRectDCS_Qpaint = QtWidgets.QLabel(Form)
        self.roundRectDCS_Qpaint.setGeometry(QtCore.QRect(pantalla_config.roundRectDCS_CoordX1-3,
                                            pantalla_config.roundRectDCS_CoordY-3,
                                            pantalla_config.roundRectDCS_HorizSize+6,
                                            pantalla_config.roundRectDCS_VertSize+6))
        self.roundRectDCS_Qpaint.setObjectName("roundRectDCS_Qpaint")
        self.canvasLabel = QtGui.QPixmap(pantalla_config.roundRectDCS_HorizSize+6,pantalla_config.roundRectDCS_VertSize+6)
        self.canvasLabel.fill(QtGui.QColor(209,209,209))
        self.roundRectDCS_Qpaint.setPixmap(self.canvasLabel)
        painter = QtGui.QPainter(self.roundRectDCS_Qpaint.pixmap())
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(50,50,50))
        brush.setStyle(1)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(255,22,25))
        painter.setPen(pen)
        painter.drawRoundedRect(3, 3,pantalla_config.roundRectDCS_HorizSize, pantalla_config.roundRectDCS_VertSize, 30, 30)
        painter.end()
        
        ### Round Rectangle For the Marcapasos
        self.roundRectMCP_Qpaint = QtWidgets.QLabel(Form)
        self.roundRectMCP_Qpaint.setGeometry(QtCore.QRect(pantalla_config.roundRectMCP_CoordX1-3,
                                            pantalla_config.roundRectMCP_CoordY-3,
                                            pantalla_config.roundRectMCP_HorizSize+6,
                                            pantalla_config.roundRectMCP_VertSize+6))
        self.roundRectMCP_Qpaint.setObjectName("roundRectMCP_Qpaint")
        self.canvasLabel = QtGui.QPixmap(pantalla_config.roundRectMCP_HorizSize+6,pantalla_config.roundRectMCP_VertSize+6)
        self.canvasLabel.fill(QtGui.QColor(209,209,209))
        self.roundRectMCP_Qpaint.setPixmap(self.canvasLabel)
        painter = QtGui.QPainter(self.roundRectMCP_Qpaint.pixmap())
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(50,50,50))
        brush.setStyle(1)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(0,129,52))
        painter.setPen(pen)
        painter.drawRoundedRect(3, 3,pantalla_config.roundRectMCP_HorizSize, pantalla_config.roundRectMCP_VertSize, 30, 30)
        painter.end()

        ### Widget de Layout vertical para la graficacion de senales 
        self.Graph_verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.Graph_verticalLayoutWidget.setGeometry(QtCore.QRect(pantalla_config.grah_CoordX1,
                                                                pantalla_config.grah_CoordY1, 
                                                                pantalla_config.grah_HorizSize, 
                                                                pantalla_config.grah_VertSize))
        self.Graph_verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Graph_verticalLayout = QtWidgets.QVBoxLayout(self.Graph_verticalLayoutWidget)
        self.plt = pg.PlotWidget()
        self.Graph_verticalLayout.addWidget(self.plt)
        self.Graph_verticalLayoutWidget.setHidden(True)

        ### todo Stacked widget
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setGeometry(QtCore.QRect(pantalla_config.stackedWidget_CoordX1,
                                                    pantalla_config.stackedWidget_CoordY1,
                                                    pantalla_config.stackedWidget_HorizSize,
                                                    pantalla_config.stackedWidget_VertSize))
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.offPage = QtWidgets.QWidget()
        self.offPage.setObjectName("offPage")
        
        self.defaultPage = QtWidgets.QWidget()
        self.defaultPage.setObjectName("defaultPage")

        self.cprPage = QtWidgets.QWidget()
        self.cprPage.setObjectName("cprPage")

        self.defibPage = QtWidgets.QWidget()
        self.defibPage.setObjectName("defibPage")

        self.pacerPage = QtWidgets.QWidget()
        self.pacerPage.setObjectName("pacerPage")

        self.stackedWidget.addWidget(self.offPage)
        self.stackedWidget.addWidget(self.defaultPage)
        self.stackedWidget.addWidget(self.cprPage)
        self.stackedWidget.addWidget(self.defibPage)
        self.stackedWidget.addWidget(self.pacerPage)

        # Round Rectangle for Vital Signals
        self.roundRectVitalSignals_Qpaint = QtWidgets.QLabel(Form)
        self.roundRectVitalSignals_Qpaint.setGeometry(QtCore.QRect(pantalla_config.roundRectVitalSignals_CoordX1-3,
                                            pantalla_config.roundRectVitalSignals_CoordY1-3,
                                            pantalla_config.roundRectVitalSignals_HorizSize+6,
                                            pantalla_config.roundRectVitalSignals_VertSize+6))
        self.roundRectVitalSignals_Qpaint.setObjectName("roundRectVitalSignals_Qpaint")
        self.canvasLabel = QtGui.QPixmap(pantalla_config.roundRectVitalSignals_HorizSize+6,pantalla_config.roundRectVitalSignals_VertSize+6)
        self.canvasColor = QtGui.QColor(209,209,209)
        self.canvasColor.setAlpha(0)
        self.canvasLabel.fill(self.canvasColor)
        self.roundRectVitalSignals_Qpaint.setPixmap(self.canvasLabel)
        painter = QtGui.QPainter(self.roundRectVitalSignals_Qpaint.pixmap())
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(34,34,34))
        brush.setStyle(1)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(34,34,34))
        painter.setPen(pen)
        painter.drawRoundedRect(3, 3,pantalla_config.roundRectVitalSignals_HorizSize, pantalla_config.roundRectVitalSignals_VertSize, 30, 30)
        painter.end()
        self.roundRectVitalSignals_Qpaint.setHidden(True)

        ### Widget Layout vertical para botones Defib, Charge, Shock
            #Push Button 
        self.DEFIB_pushButton = QtWidgets.QPushButton(Form)
        self.DEFIB_pushButton.setGeometry(QtCore.QRect(pantalla_config.DEFIB_CoordX1,
                                                        pantalla_config.DEFIB_CoordY1,
                                                        pantalla_config.DEFIB_HorizSize,
                                                        pantalla_config.DEFIB_VertSize))
        self.DEFIB_pushButton.setObjectName("DEFIB_pushButton")
        self.Charge_pushButton = QtWidgets.QPushButton(Form)
        self.Charge_pushButton.setGeometry(QtCore.QRect(pantalla_config.CHARGE_CoordX1,
                                                        pantalla_config.CHARGE_CoordY1,
                                                        pantalla_config.CHARGE_HorizSize,
                                                        pantalla_config.CHARGE_VertSize))
        self.Charge_pushButton.setObjectName("Charge_pushButton")

        self.Shock_pushButton = QtWidgets.QPushButton(Form)
        self.Shock_pushButton.setGeometry(QtCore.QRect(pantalla_config.SHOCK_CoordX1,
                                                        pantalla_config.SHOCK_CoordY1,
                                                        pantalla_config.SHOCK_HorizSize,
                                                        pantalla_config.SHOCK_VertSize))
        self.Shock_pushButton.setObjectName("Shock_pushButton")
            #StyleSheet Button
        self.DEFIB_pushButton.setStyleSheet(Stylesheet)
        self.Charge_pushButton.setStyleSheet(Stylesheet)
        self.Shock_pushButton.setStyleSheet(Stylesheet)
        
        ### Button Play, Pause, Stop, Question
        self.PPSQBackground_pushButton = QtWidgets.QPushButton(Form)
        self.PPSQBackground_pushButton.setGeometry(QtCore.QRect(pantalla_config.PPSQBackground_CoordX1,
                                                                pantalla_config.PPSQBackground_CoordY1,
                                                                pantalla_config.PPSQBackground_HorizSize,
                                                                pantalla_config.PPSQBackground_VertSize))
        self.PPSQBackground_pushButton.setObjectName("PPSQBackground_pushButton")
        self.PPSQBackground_pushButton.setStyleSheet(Stylesheet)
            #Button
        self.play_RoundButton = QtWidgets.QPushButton(Form, icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Play_icon.svg")))
        play_RoundButtonSize = self.play_RoundButton.size()
        self.play_RoundButton.setIconSize(QtCore.QSize(round(play_RoundButtonSize.width()*0.8), round(play_RoundButtonSize.height()*0.8)))
        self.play_RoundButton.setGeometry(QtCore.QRect(pantalla_config.play_CoordX1,
                                                    pantalla_config.play_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.play_RoundButton.setObjectName("play_RoundButton")
        self.play_RoundButton.setStyleSheet(Stylesheet)

        self.pause_RoundButton = QtWidgets.QPushButton(Form, icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Pause_icon.svg")))
        self.pause_RoundButtonSize = self.pause_RoundButton.size()
        self.pause_RoundButton.setIconSize(QtCore.QSize(round(self.pause_RoundButtonSize.width()*0.80), round(self.pause_RoundButtonSize.height()*0.8)))
        self.pause_RoundButton.setGeometry(QtCore.QRect(pantalla_config.pause_CoordX1,
                                                    pantalla_config.pause_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.pause_RoundButton.setObjectName("pause_RoundButton")
        self.pause_RoundButton.setStyleSheet(Stylesheet)

        self.stop_RoundButton = QtWidgets.QPushButton(Form, icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Stop_icon.svg")))
        self.stop_RoundButtonSize = self.stop_RoundButton.size()
        self.stop_RoundButton.setIconSize(QtCore.QSize(round(self.stop_RoundButtonSize.width()*0.60), round(self.stop_RoundButtonSize.height()*0.60)))
        self.stop_RoundButton.setGeometry(QtCore.QRect(pantalla_config.stop_CoordX1,
                                                    pantalla_config.stop_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.stop_RoundButton.setObjectName("stop_RoundButton")
        self.stop_RoundButton.setStyleSheet(Stylesheet)
        
        self.question_RoundButton = QtWidgets.QPushButton(Form, icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Question_icon.svg")))
        self.question_RoundButtonSize = self.question_RoundButton.size()
        self.question_RoundButton.setIconSize(QtCore.QSize(self.question_RoundButtonSize.width(), self.question_RoundButtonSize.height()))
        self.question_RoundButton.setGeometry(QtCore.QRect(pantalla_config.question_CoordX1,
                                                    pantalla_config.question_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.question_RoundButton.setObjectName("question_RoundButton")
        self.question_RoundButton.setStyleSheet(Stylesheet)

        self.OnOff_RoundButton = QtWidgets.QPushButton(Form, icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/OnOFF_Icon.svg")))
        self.OnOff_RoundButtonSize = self.OnOff_RoundButton.size()
        self.OnOff_RoundButton.setIconSize(QtCore.QSize(self.OnOff_RoundButtonSize.width(), self.OnOff_RoundButtonSize.height()))
        self.OnOff_RoundButton.setGeometry(QtCore.QRect(pantalla_config.OnOff_CoordX1,
                                                    pantalla_config.OnOff_CoordY1,
                                                    pantalla_config.OnOff_VertSize,
                                                    pantalla_config.OnOff_VertSize))
        self.OnOff_RoundButton.setObjectName("OnOff_RoundButton")
        self.OnOff_RoundButton.setStyleSheet(Stylesheet)

            #StyleSheet

        ### Energy Select, Dea and Sync Buttons
            # Up Energey Select (UES)
        self.UpEnergySelect_pushButton = QtWidgets.QPushButton(Form, icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Up_icon.svg")))
        UpEnergySelect_buttonSize = self.UpEnergySelect_pushButton.size()
        self.UpEnergySelect_pushButton.setIconSize(QtCore.QSize(UpEnergySelect_buttonSize.width(), UpEnergySelect_buttonSize.height()))
        self.UpEnergySelect_pushButton.setGeometry(QtCore.QRect(pantalla_config.UES_CoordX1,
                                                                pantalla_config.UES_CoordY1,
                                                                pantalla_config.UES_HorizSize,
                                                                pantalla_config.UES_VertSize))
        self.UpEnergySelect_pushButton.setObjectName("UpEnergySelect_pushButton")
        self.UpEnergySelect_pushButton.setStyleSheet(Stylesheet)
            # Down Energey Select (DES)
        self.DownEnergySelect_pushButton = QtWidgets.QPushButton(Form,icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Down_icon.svg")))
        self.DownEnergySelect_buttonSize = self.DownEnergySelect_pushButton.size()
        self.DownEnergySelect_pushButton.setIconSize(QtCore.QSize(self.DownEnergySelect_buttonSize.width(), self.DownEnergySelect_buttonSize.height()))
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

        self.DISCHARGE_pushButton = QtWidgets.QPushButton(Form)
        self.DISCHARGE_pushButton.setGeometry(QtCore.QRect(pantalla_config.DISCHARGE_CoordX1,
                                                    pantalla_config.DISCHARGE_CoordY1,
                                                    pantalla_config.DISCHARGE_HorizSize,
                                                    pantalla_config.DISCHARGE_VertSize))
        self.DISCHARGE_pushButton.setObjectName("DISCHARGE_pushButton")
        self.DISCHARGE_pushButton.setStyleSheet(Stylesheet)

        ## MARCP Buttons
        self.UPO_pushButton = QtWidgets.QPushButton(Form,icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Up_icon.svg")))
        self.UPO_buttonSize = self.UPO_pushButton.size()
        self.UPO_pushButton.setIconSize(QtCore.QSize(self.UPO_buttonSize.width(),self.UPO_buttonSize.height()))
        self.UPO_pushButton.setGeometry(QtCore.QRect(pantalla_config.UPO_CoordX1,
                                                    pantalla_config.UPO_CoordY,
                                                    pantalla_config.UPO_HorizSize,
                                                    pantalla_config.UPO_VertSize))
        self.UPO_pushButton.setObjectName("UPO_pushButton")
        self.UPO_pushButton.setStyleSheet(Stylesheet)

        self.DPO_pushButton = QtWidgets.QPushButton(Form,icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Down_icon.svg")))
        self.DPO_buttonSize = self.DPO_pushButton.size()
        self.DPO_pushButton.setIconSize(QtCore.QSize(self.DPO_buttonSize.width(),self.DPO_buttonSize.height()))
        self.DPO_pushButton.setGeometry(QtCore.QRect(pantalla_config.DPO_CoordX1,
                                                    pantalla_config.DPO_CoordY,
                                                    pantalla_config.DPO_HorizSize,
                                                    pantalla_config.DPO_VertSize))
        self.DPO_pushButton.setObjectName("DPO_pushButton")
        self.DPO_pushButton.setStyleSheet(Stylesheet)

        self.UPR_pushButton = QtWidgets.QPushButton(Form,icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Up_icon.svg")))
        self.UPR_buttonSize = self.UPR_pushButton.size()
        self.UPR_pushButton.setIconSize(QtCore.QSize(self.UPR_buttonSize.width(),self.UPR_buttonSize.height()))
        self.UPR_pushButton.setGeometry(QtCore.QRect(pantalla_config.UPR_CoordX1,
                                                    pantalla_config.UPR_CoordY,
                                                    pantalla_config.UPR_HorizSize,
                                                    pantalla_config.UPR_VertSize))
        self.UPR_pushButton.setObjectName("UPR_pushButton")
        self.UPR_pushButton.setStyleSheet(Stylesheet)

        self.DPR_pushButton = QtWidgets.QPushButton(Form,icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Down_icon.svg")))
        self.DPR_buttonSize = self.DPR_pushButton.size()
        self.DPR_pushButton.setIconSize(QtCore.QSize(self.DPR_buttonSize.width(), self.DPR_buttonSize.height()))
        self.DPR_pushButton.setGeometry(QtCore.QRect(pantalla_config.DPR_CoordX1,
                                                    pantalla_config.DPR_CoordY,
                                                    pantalla_config.DPR_HorizSize,
                                                    pantalla_config.DPR_VertSize))
        self.DPR_pushButton.setObjectName("DPR_pushButton")
        self.DPR_pushButton.setStyleSheet(Stylesheet)

        ## Bottom Menu
        self.confirmMenu_pushButton = QtWidgets.QPushButton(Form)
        self.confirmMenu_pushButton.setGeometry(QtCore.QRect(pantalla_config.confirmMenu_CoordX1 ,
                                                            pantalla_config.confirmMenu_CoordY ,
                                                            pantalla_config.confirmMenu_HorizSize ,
                                                            pantalla_config.confirmMenu_VertSize ))
        self.confirmMenu_pushButton.setObjectName("confirmMenu_pushButton")
        self.confirmMenu_pushButton.setStyleSheet(Stylesheet)

        self.returnMenu_pushButton = QtWidgets.QPushButton(Form)
        self.returnMenu_pushButton.setGeometry(QtCore.QRect(pantalla_config.returnMenu_CoordX1 ,
                                                            pantalla_config.returnMenu_CoordY ,
                                                            pantalla_config.returnMenu_HorizSize ,
                                                            pantalla_config.returnMenu_VertSize ))
        self.returnMenu_pushButton.setObjectName("returnMenu_pushButton")
        self.returnMenu_pushButton.setStyleSheet(Stylesheet)

        self.paniMenu_pushButton = QtWidgets.QPushButton(Form)
        self.paniMenu_pushButton.setGeometry(QtCore.QRect(pantalla_config.paniMenu_CoordX1,
                                                        pantalla_config.paniMenu_CoordY,
                                                        pantalla_config.paniMenu_HorizSize,
                                                        pantalla_config.paniMenu_VertSize))
        self.paniMenu_pushButton.setObjectName("paniMenu_pushButton")
        self.paniMenu_pushButton.setStyleSheet(Stylesheet)

        self.alarmMenu_pushButton = QtWidgets.QPushButton(Form)
        self.alarmMenu_pushButton.setGeometry(QtCore.QRect(pantalla_config.alarmMenu_CoordX1 ,
                                                            pantalla_config.alarmMenu_CoordY ,
                                                            pantalla_config.alarmMenu_HorizSize ,
                                                            pantalla_config.alarmMenu_VertSize ))
        self.alarmMenu_pushButton.setObjectName("alarmMenu_pushButton")
        self.alarmMenu_pushButton.setStyleSheet(Stylesheet)

        self.CPRMenu_pushButton = QtWidgets.QPushButton(Form)
        self.CPRMenu_pushButton.setGeometry(QtCore.QRect(pantalla_config.CPRMenu_CoordX1 ,
                                                            pantalla_config.CPRMenu_CoordY ,
                                                            pantalla_config.CPRMenu_HorizSize ,
                                                            pantalla_config.CPRMenu_VertSize ))
        self.CPRMenu_pushButton.setObjectName("CPRMenu_pushButton")
        self.CPRMenu_pushButton.setStyleSheet(Stylesheet)

        self.sizeMenu_pushButton = QtWidgets.QPushButton(Form)
        self.sizeMenu_pushButton.setGeometry(QtCore.QRect(pantalla_config.sizeMenu_CoordX1 ,
                                                            pantalla_config.sizeMenu_CoordY ,
                                                            pantalla_config.sizeMenu_HorizSize ,
                                                            pantalla_config.sizeMenu_VertSize ))
        self.sizeMenu_pushButton.setObjectName("sizeMenu_pushButton")
        self.sizeMenu_pushButton.setStyleSheet(Stylesheet)

        self.LEADMenu_pushButton = QtWidgets.QPushButton(Form)
        self.LEADMenu_pushButton.setGeometry(QtCore.QRect(pantalla_config.LEADMenu_CoordX1 ,
                                                            pantalla_config.LEADMenu_CoordY ,
                                                            pantalla_config.LEADMenu_HorizSize ,
                                                            pantalla_config.LEADMenu_VertSize ))
        self.LEADMenu_pushButton.setObjectName("LEADMenu_pushButton")
        self.LEADMenu_pushButton.setStyleSheet(Stylesheet)

        ## Round triangle buttons 
        self.DownRoundTriangle = DOWNRoundTriangle(Form)
        self.DownRoundTriangle.setGeometry(QtCore.QRect(pantalla_config.DTriangle_CoordX1,
                                                    pantalla_config.DTriangle_CoordY1,
                                                    pantalla_config.Triangle_RoundButtonSize+10,
                                                    pantalla_config.Triangle_RoundButtonSize+10))
        self.DownRoundTriangle.setObjectName("DownRoundTriangle")


        self.UpRoundTriangle = UPRoundTriangle(Form)
        self.UpRoundTriangle.setGeometry(QtCore.QRect(pantalla_config.UTriangle_CoordX1,
                                                    pantalla_config.UTriangle_CoordY1,
                                                    pantalla_config.Triangle_RoundButtonSize,
                                                    pantalla_config.Triangle_RoundButtonSize))
        self.UpRoundTriangle.setObjectName("UpRoundTriangle")

        # Energy select red button label 
        self.energySelectLabel_pushButton = QtWidgets.QPushButton(Form)
        self.energySelectLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.energySelectLabel_CoordX1 ,
                                                                    pantalla_config.energySelectLabel_CoordY ,
                                                                    pantalla_config.energySelectLabel_HorizSize ,
                                                                    pantalla_config.energySelectLabel_VertSize))
        self.energySelectLabel_pushButton.setObjectName("energySelectLabel_pushButton")
        self.energySelectLabel_pushButton.setStyleSheet(Stylesheet)
        
        self.MARCPLabel_pushButton = QtWidgets.QPushButton(Form)
        self.MARCPLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.MARCPLabel_CoordX1 ,
                                                                    pantalla_config.MARCPLabel_CoordY ,
                                                                    pantalla_config.MARCPLabel_HorizSize ,
                                                                    pantalla_config.MARCPLabel_VertSize))
        self.MARCPLabel_pushButton.setObjectName("MARCPLabel_pushButton")
        self.MARCPLabel_pushButton.setStyleSheet(Stylesheet)

        self.mALabel_pushButton = QtWidgets.QPushButton(Form)
        self.mALabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.mALabel_CoordX1 ,
                                                                    pantalla_config.mALabel_CoordY ,
                                                                    pantalla_config.mALabel_HorizSize ,
                                                                    pantalla_config.mALabel_VertSize))
        self.mALabel_pushButton.setObjectName("mALabel_pushButton")
        self.mALabel_pushButton.setStyleSheet(Stylesheet)

        self.PPMLabel_pushButton = QtWidgets.QPushButton(Form)
        self.PPMLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.PPMLabel_CoordX1 ,
                                                                    pantalla_config.PPMLabel_CoordY ,
                                                                    pantalla_config.PPMLabel_HorizSize ,
                                                                    pantalla_config.PPMLabel_VertSize))
        self.PPMLabel_pushButton.setObjectName("PPMLabel_pushButton")
        self.PPMLabel_pushButton.setStyleSheet(Stylesheet)

        self.pacerOutput_Label = QtWidgets.QLabel(Form)
        self.pacerOutput_Label.setGeometry(QtCore.QRect(pantalla_config.pacerOutputLabel_CoordX1 ,
                                                        pantalla_config.pacerOutputLabel_CoordY ,
                                                        pantalla_config.pacerOutputLabel_HorizSize ,
                                                        pantalla_config.pacerOutputLabel_VertSize ))
        self.pacerOutput_Label.setObjectName("pacerOutput_Label")                                                
        self.pacerOutput_Label.setStyleSheet(Stylesheet)

        self.pacerRate_Label = QtWidgets.QLabel(Form)
        self.pacerRate_Label.setGeometry(QtCore.QRect(pantalla_config.pacerRateLabel_CoordX1 ,
                                                        pantalla_config.pacerRateLabel_CoordY ,
                                                        pantalla_config.pacerRateLabel_HorizSize ,
                                                        pantalla_config.pacerRateLabel_VertSize ))
        self.pacerRate_Label.setObjectName("pacerRate_Label")
        self.pacerRate_Label.setStyleSheet(Stylesheet)

        self.config_pushButton = QtWidgets.QPushButton(Form, icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Config_icon.svg")))
        self.config_pushButtonSize = self.config_pushButton.size()
        self.config_pushButton.setIconSize(QtCore.QSize(self.OnOff_RoundButtonSize.width(), self.OnOff_RoundButtonSize.height()))
        self.config_pushButton.setGeometry(QtCore.QRect(pantalla_config.config_CoordX1,
                                                        pantalla_config.config_CoordY,
                                                        pantalla_config.PPSQ_RoundButtonSize,
                                                        pantalla_config.PPSQ_RoundButtonSize))
        self.config_pushButton.setObjectName("config_pushButton")
        self.config_pushButton.setStyleSheet(Stylesheet)

        self.version_Label = QtWidgets.QLabel(Form)
        self.version_Label.setGeometry(QtCore.QRect(pantalla_config.versionLabel_CoordX1,
                                                    pantalla_config.versionLabel_CoordY,
                                                    pantalla_config.versionLabel_HorizSize,
                                                    pantalla_config.versionLabel_VertSize))
        self.version_Label.setObjectName("version_Label")
        self.version_Label.setStyleSheet(Stylesheet)

        # Logo de KabSinLogo
        # self.KabSinLogo_horizontalLayoutWidget = QtWidgets.QWidget(Form)
        # self.KabSinLogo_horizontalLayoutWidget.setGeometry(QtCore.QRect(pantalla_config.KabSimLogo_CoordX1,
        #                                                                 pantalla_config.KabSimLogo_CoordY,
        #                                                                 pantalla_config.KabSimLogo_HorizSize,
        #                                                                 pantalla_config.KabSimLogo_VertSize))
        # self.KabSinLogo_horizontalLayoutWidget.setObjectName("KabSinLogo_horizontalLayoutWidget")
        # self.KabSinLogo_horizontalLayout = QtWidgets.QHBoxLayout(self.KabSinLogo_horizontalLayoutWidget)
        # self.KabSinLogo_horizontalLayout.setContentsMargins(0, 0, 0, 0)
        # self.KabSinLogo_horizontalLayout.setObjectName("KabSinLogo_horizontalLayout")

        # self.KabSimLogo_Scene = QtWidgets.QGraphicsScene(0, 0, self.KabSinLogo_horizontalLayoutWidget.width(), self.KabSinLogo_horizontalLayoutWidget.height())
        # self.KabSimLogo_Path = "PyQt_Images/Abersiya.svg"
        # self.KabSimLogo_Image = QtGui.QPixmap(self.KabSimLogo_Path)
        # self.KabSimLogo_pixmapitem = self.KabSimLogo_Scene.addPixmap(self.KabSimLogo_Image.scaled(self.KabSimLogo_Scene.sceneRect().size().toSize()))
        # self.KabSimLogo_pixmapitem.setPos(0,0)
        
        
        # self.KabSimLogo_view = QtWidgets.QGraphicsView(self.KabSimLogo_Scene)
        # self.KabSimLogo_view.setRenderHint(QtGui.QPainter.Antialiasing)
        # self.KabSimLogo_view.setStyleSheet("border: none;background-color: rgb(209,209,209);")
        # self.KabSinLogo_horizontalLayout.addWidget(self.KabSimLogo_view)
        
        self.simulationTimeValue_pushButton = QtWidgets.QPushButton(Form)
        self.simulationTimeValue_pushButton.setGeometry(QtCore.QRect(pantalla_config.simulationTimeValue_CoordX1,
                                                                    pantalla_config.simulationTimeValue_CoordY,
                                                                    pantalla_config.simulationTimeValue_HorizSize,
                                                                    pantalla_config.simulationTimeValue_VertSize))
        self.simulationTimeValue_pushButton.setObjectName("simulationTimeValue_pushButton")
        self.simulationTimeValue_pushButton.setStyleSheet(Stylesheet)
        self.simulationTimeValue_pushButton.setHidden(True)

        self.simulationTimeLabel_Label = QtWidgets.QLabel(Form)
        self.simulationTimeLabel_Label.setGeometry(QtCore.QRect(pantalla_config.simulationTimeLabel_CoordX1,
                                                                pantalla_config.simulationTimeLabel_CoordY,
                                                                pantalla_config.simulationTimeLabel_HorizSize,
                                                                pantalla_config.simulationTimeLabel_VertSize))
        self.simulationTimeLabel_Label.setHidden(True)

        self.heartRateLabel_pushButton = QtWidgets.QPushButton(Form)
        self.heartRateLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.heartRateLabel_CoordX1,
                                                            pantalla_config.heartRateLabel_CoordY,
                                                            pantalla_config.heartRateLabel_HorizSize,
                                                            pantalla_config.heartRateLabel_VertSize))
        self.heartRateLabel_pushButton.setObjectName("heartRateLabel_pushButton")
        self.heartRateLabel_pushButton.setStyleSheet(Stylesheet)
        self.heartRateLabel_pushButton.setHidden(True)

        self.heartRateValue_Label = QtWidgets.QLabel(Form)
        self.heartRateValue_Label.setGeometry(QtCore.QRect(pantalla_config.heartRateValueLabel_CoordX1,
                                                            pantalla_config.heartRateValueLabel_CoordY,
                                                            pantalla_config.heartRateValueLabel_HorizSize,
                                                            pantalla_config.heartRateValueLabel_VertSize))
        self.heartRateValue_Label.setObjectName("heartRateValue_Label")
        self.heartRateValue_Label.setStyleSheet(Stylesheet)
        self.heartRateValue_Label.setHidden(True)

        self.heartRateUnidades_Label = QtWidgets.QLabel(Form)
        self.heartRateUnidades_Label.setGeometry(QtCore.QRect(pantalla_config.heartRateUnidadesLabel_CoordX1,
                                                                pantalla_config.heartRateUnidadesLabel_CoordY,
                                                                pantalla_config.heartRateUnidadesLabel_HorizSize,
                                                                pantalla_config.heartRateUnidadesLabel_VertSize))
        self.heartRateUnidades_Label.setObjectName("heartRateUnidades_Label")
        self.heartRateUnidades_Label.setStyleSheet(Stylesheet)
        self.heartRateUnidades_Label.setHidden(True)

        self.tempLabel_pushButton = QtWidgets.QPushButton(Form)
        self.tempLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.tempLabel_CoordX1,
                                                        pantalla_config.tempLabel_CoordY,
                                                        pantalla_config.tempLabel_HorizSize,
                                                        pantalla_config.tempLabel_VertSize))
        self.tempLabel_pushButton.setObjectName("tempLabel_pushButton")
        self.tempLabel_pushButton.setStyleSheet(Stylesheet)
        self.tempLabel_pushButton.setHidden(True)

        self.tempValue_Label = QtWidgets.QLabel(Form)
        self.tempValue_Label.setGeometry(QtCore.QRect(pantalla_config.tempValueLabel_CoordX1,
                                                            pantalla_config.tempValueLabel_CoordY,
                                                            pantalla_config.tempValueLabel_HorizSize,
                                                            pantalla_config.tempValueLabel_VertSize))
        self.tempValue_Label.setObjectName("tempValue_Label")
        self.tempValue_Label.setStyleSheet(Stylesheet)
        self.tempValue_Label.setHidden(True)

        self.tempUnidades_Label = QtWidgets.QLabel(Form)
        self.tempUnidades_Label.setGeometry(QtCore.QRect(pantalla_config.tempUnidadesLabel_CoordX1,
                                                                pantalla_config.tempUnidadesLabel_CoordY,
                                                                pantalla_config.tempUnidadesLabel_HorizSize,
                                                                pantalla_config.tempUnidadesLabel_VertSize))
        self.tempUnidades_Label.setObjectName("tempUnidades_Label")
        self.tempUnidades_Label.setStyleSheet(Stylesheet)
        self.tempUnidades_Label.setHidden(True)

        self.SpO2Label_pushButton = QtWidgets.QPushButton(Form)
        self.SpO2Label_pushButton.setGeometry(QtCore.QRect(pantalla_config.SpO2Label_CoordX1,
                                                    pantalla_config.SpO2Label_CoordY,
                                                    pantalla_config.SpO2Label_HorizSize,
                                                    pantalla_config.SpO2Label_VertSize))
        self.SpO2Label_pushButton.setObjectName("SpO2Label_pushButton")
        self.SpO2Label_pushButton.setStyleSheet(Stylesheet)
        self.SpO2Label_pushButton.setHidden(True)

        self.SpO2Value_Label = QtWidgets.QLabel(Form)
        self.SpO2Value_Label.setGeometry(QtCore.QRect( pantalla_config.SpO2ValueLabel_CoordX1,
                                                            pantalla_config.SpO2ValueLabel_CoordY,
                                                            pantalla_config.SpO2ValueLabel_HorizSize,
                                                            pantalla_config.SpO2ValueLabel_VertSize))
        self.SpO2Value_Label.setObjectName("SpO2Value_Label")
        self.SpO2Value_Label.setStyleSheet(Stylesheet)
        self.SpO2Value_Label.setHidden(True)

        self.SpO2Unidades_Label = QtWidgets.QLabel(Form)
        self.SpO2Unidades_Label.setGeometry(QtCore.QRect(pantalla_config.SpO2UnidadesLabel_CoordX1,
                                                                pantalla_config.SpO2UnidadesLabel_CoordY,
                                                                pantalla_config.SpO2UnidadesLabel_HorizSize,
                                                                pantalla_config.SpO2UnidadesLabel_VertSize))
        self.SpO2Unidades_Label.setObjectName("SpO2Unidades_Label")
        self.SpO2Unidades_Label.setStyleSheet(Stylesheet)
        self.SpO2Unidades_Label.setHidden(True)
        
        self.pressureLabel_pushButton = QtWidgets.QPushButton(Form)
        self.pressureLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.pressureLabel_CoordX1,
                                                        pantalla_config.pressureLabel_CoordY,
                                                        pantalla_config.pressureLabel_HorizSize,
                                                        pantalla_config.pressureLabel_VertSize))
        self.pressureLabel_pushButton.setObjectName("pressureLabel_pushButton")
        self.pressureLabel_pushButton.setStyleSheet(Stylesheet)
        self.pressureLabel_pushButton.setHidden(True)

        self.pressureValue_Label = QtWidgets.QLabel(Form)
        self.pressureValue_Label.setGeometry(QtCore.QRect(pantalla_config.pressureValueLabel_CoordX1,
                                                            pantalla_config.pressureValueLabel_CoordY,
                                                            pantalla_config.pressureValueLabel_HorizSize,
                                                            pantalla_config.pressureValueLabel_VertSize))
        self.pressureValue_Label.setObjectName("pressureValue_Label")
        self.pressureValue_Label.setStyleSheet(Stylesheet)
        self.pressureValue_Label.setHidden(True)

        self.pressureUnidades_Label = QtWidgets.QLabel(Form)
        self.pressureUnidades_Label.setGeometry(QtCore.QRect(pantalla_config.pressureUnidadesLabel_CoordX1,
                                                                pantalla_config.pressureUnidadesLabel_CoordY,
                                                                pantalla_config.pressureUnidadesLabel_HorizSize,
                                                                pantalla_config.pressureUnidadesLabel_VertSize))
        self.pressureUnidades_Label.setObjectName("pressureUnidades_Label")
        self.pressureUnidades_Label.setStyleSheet(Stylesheet)
        self.pressureUnidades_Label.setHidden(True)

        self.FRLabel_pushButton = QtWidgets.QPushButton(Form)
        self.FRLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.FRLabel_CoordX1,
                                                    pantalla_config.FRLabel_CoordY,
                                                    pantalla_config.FRLabel_HorizSize,
                                                    pantalla_config.FRLabel_VertSize))
        self.FRLabel_pushButton.setObjectName("FRLabel_pushButton")
        self.FRLabel_pushButton.setStyleSheet(Stylesheet)
        self.FRLabel_pushButton.setHidden(True)

        self.FRValue_Label = QtWidgets.QLabel(Form)
        self.FRValue_Label.setGeometry(QtCore.QRect( pantalla_config.FRValueLabel_CoordX1,
                                                            pantalla_config.FRValueLabel_CoordY,
                                                            pantalla_config.FRValueLabel_HorizSize,
                                                            pantalla_config.FRValueLabel_VertSize))
        self.FRValue_Label.setObjectName("FRValue_Label")
        self.FRValue_Label.setStyleSheet(Stylesheet)
        self.FRValue_Label.setHidden(True)

        self.FRUnidades_Label = QtWidgets.QLabel(Form)
        self.FRUnidades_Label.setGeometry(QtCore.QRect(pantalla_config.FRUnidadesLabel_CoordX1,
                                                                pantalla_config.FRUnidadesLabel_CoordY,
                                                                pantalla_config.FRUnidadesLabel_HorizSize,
                                                                pantalla_config.FRUnidadesLabel_VertSize))
        self.FRUnidades_Label.setObjectName("FRUnidades_Label")
        self.FRUnidades_Label.setStyleSheet(Stylesheet)
        self.FRUnidades_Label.setHidden(True)

        self.CO2Label_pushButton = QtWidgets.QPushButton(Form)
        self.CO2Label_pushButton.setGeometry(QtCore.QRect(pantalla_config.CO2Label_CoordX1,
                                                        pantalla_config.CO2Label_CoordY,
                                                        pantalla_config.CO2Label_HorizSize,
                                                        pantalla_config.CO2Label_VertSize))
        self.CO2Label_pushButton.setObjectName("CO2Label_pushButton")
        self.CO2Label_pushButton.setStyleSheet(Stylesheet)
        self.CO2Label_pushButton.setHidden(True)

        self.CO2Value_Label = QtWidgets.QLabel(Form)
        self.CO2Value_Label.setGeometry(QtCore.QRect(pantalla_config.CO2ValueLabel_CoordX1,
                                                            pantalla_config.CO2ValueLabel_CoordY,
                                                            pantalla_config.CO2ValueLabel_HorizSize,
                                                            pantalla_config.CO2ValueLabel_VertSize))
        self.CO2Value_Label.setObjectName("CO2Value_Label")
        self.CO2Value_Label.setStyleSheet(Stylesheet)
        self.CO2Value_Label.setHidden(True)

        self.CO2Unidades_Label = QtWidgets.QLabel(Form)
        self.CO2Unidades_Label.setGeometry(QtCore.QRect(pantalla_config.CO2UnidadesLabel_CoordX1,
                                                                pantalla_config.CO2UnidadesLabel_CoordY,
                                                                pantalla_config.CO2UnidadesLabel_HorizSize,
                                                                pantalla_config.CO2UnidadesLabel_VertSize))
        self.CO2Unidades_Label.setObjectName("CO2Unidades_Label")
        self.CO2Unidades_Label.setStyleSheet(Stylesheet)
        self.CO2Unidades_Label.setHidden(True)

        self.port_comboBox = QtWidgets.QComboBox(Form)
        self.port_comboBox.setGeometry(QtCore.QRect(pantalla_config.port_CoordX1,
                                                    pantalla_config.port_CoordY1,
                                                    pantalla_config.port_HorizSize,
                                                    pantalla_config.port_VertSize))
        self.port_comboBox.setObjectName("returnMenu_pushButton")
        self.port_comboBox.setStyleSheet(Stylesheet)

        self.CPRLabel_pushButton = QtWidgets.QPushButton(self.cprPage)
        self.CPRLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.CRPLabel_CoordX1,
                                                        pantalla_config.CRPLabel_CoordY1,
                                                        pantalla_config.CRPLabel_HorizSize,
                                                        pantalla_config.CRPLabel_VertSize))
        self.CPRLabel_pushButton.setObjectName("CPRLabel_pushButton")
        self.CPRLabel_pushButton.setStyleSheet(Stylesheet)

        self.CRPRateLabel_Label = QtWidgets.QLabel(self.cprPage)
        self.CRPRateLabel_Label.setGeometry(QtCore.QRect(pantalla_config.CRPRateLabel_CoordX1,
                                            pantalla_config.CRPRateLabel_CoordY1,
                                            pantalla_config.CRPRateLabel_HorizSize,
                                            pantalla_config.CRPRateLabel_VertSize))
        self.CRPRateLabel_Label.setObjectName("CRPRateLabel_Label")
        self.CRPRateLabel_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.CRPRateLabel_Label.setStyleSheet(Stylesheet)

        self.CRPRateValue_Label = QtWidgets.QLabel(self.cprPage)
        self.CRPRateValue_Label.setGeometry(QtCore.QRect(pantalla_config.CRPRateValue_CoordX1,
                                            pantalla_config.CRPRateValue_CoordY1,
                                            pantalla_config.CRPRateValue_HorizSize,
                                            pantalla_config.CRPRateValue_VertSize))
        self.CRPRateValue_Label.setObjectName("CRPRateValue_Label")
        self.CRPRateValue_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.CRPRateValue_Label.setStyleSheet(Stylesheet)

        self.CRPTimeLabel_Label = QtWidgets.QLabel(self.cprPage)
        self.CRPTimeLabel_Label.setGeometry(QtCore.QRect(pantalla_config.CRPTimeLabel_CoordX1,
                                            pantalla_config.CRPTimeLabel_CoordY1,
                                            pantalla_config.CRPTimeLabel_HorizSize,
                                            pantalla_config.CRPTimeLabel_VertSize))
        self.CRPTimeLabel_Label.setObjectName("CRPTimeLabel_Label")
        self.CRPTimeLabel_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.CRPTimeLabel_Label.setStyleSheet(Stylesheet)

        self.CRPTimeValue_Label = QtWidgets.QLabel(self.cprPage)
        self.CRPTimeValue_Label.setGeometry(QtCore.QRect(pantalla_config.CRPTimeValue_CoordX1,
                                            pantalla_config.CRPTimeValue_CoordY1,
                                            pantalla_config.CRPTimeValue_HorizSize,
                                            pantalla_config.CRPTimeValue_VertSize))
        self.CRPTimeValue_Label.setObjectName("CRPTimeValue_Label")
        self.CRPTimeValue_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.CRPTimeValue_Label.setStyleSheet(Stylesheet)

        self.CRPFCTLabel_Label = QtWidgets.QLabel(self.cprPage)
        self.CRPFCTLabel_Label.setGeometry(QtCore.QRect(pantalla_config.CRPFCTLabel_CoordX1,
                                            pantalla_config.CRPFCTLabel_CoordY1,
                                            pantalla_config.CRPFCTLabel_HorizSize,
                                            pantalla_config.CRPFCTLabel_VertSize))
        self.CRPFCTLabel_Label.setObjectName("CRPFCTLabel_Label")
        self.CRPFCTLabel_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.CRPFCTLabel_Label.setStyleSheet(Stylesheet)

        self.CRPFCTValue_Label = QtWidgets.QLabel(self.cprPage)
        self.CRPFCTValue_Label.setGeometry(QtCore.QRect(pantalla_config.CRPFCTValue_CoordX1,
                                            pantalla_config.CRPFCTValue_CoordY1,
                                            pantalla_config.CRPFCTValue_HorizSize,
                                            pantalla_config.CRPFCTValue_VertSize))
        self.CRPFCTValue_Label.setObjectName("CRPFCTValue_Label")
        self.CRPFCTValue_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.CRPFCTValue_Label.setStyleSheet(Stylesheet)

        self.defibLabel_pushButton = QtWidgets.QPushButton(self.defibPage)
        self.defibLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.defibLabel_CoordX1,
                                                pantalla_config.defibLabel_CoordY1,
                                                pantalla_config.defibLabel_HorizSize,
                                                pantalla_config.defibLabel_VertSize))
        self.defibLabel_pushButton.setObjectName("defibLabel_pushButton")
        self.defibLabel_pushButton.setStyleSheet(Stylesheet)

        self.pacerLabel_pushButton =QtWidgets.QPushButton(self.pacerPage)
        self.pacerLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.pacerLabel_CoordX1,
                                                pantalla_config.pacerLabel_CoordY1,
                                                pantalla_config.pacerLabel_HorizSize,
                                                pantalla_config.pacerLabel_VertSize))
        self.pacerLabel_pushButton.setObjectName("pacerLabel_pushButton")
        self.pacerLabel_pushButton.setStyleSheet(Stylesheet)

        self.pacerLabelText_Label = QtWidgets.QLabel(self.pacerPage)
        self.pacerLabelText_Label.setGeometry(QtCore.QRect(pantalla_config.pacerLabelText_CoordX1,
                                                            pantalla_config.pacerLabelText_CoordY1,
                                                            pantalla_config.pacerLabelText_HorizSize,
                                                            pantalla_config.pacerLabelText_VertSize))
        self.pacerLabelText_Label.setObjectName("pacerLabelText_Label")
        self.pacerLabelText_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.pacerLabelText_Label.setStyleSheet(Stylesheet)

        self.pacerValuemA_Label = QtWidgets.QLabel(self.pacerPage)
        self.pacerValuemA_Label.setGeometry(QtCore.QRect(pantalla_config.pacerValuemA_CoordX1,
                                                        pantalla_config.pacerValuemA_CoordY1,
                                                        pantalla_config.pacerValuemA_HorizSize,
                                                        pantalla_config.pacerValuemA_VertSize))
        self.pacerValuemA_Label.setObjectName("pacerValuemA_Label")
        self.pacerValuemA_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.pacerValuemA_Label.setStyleSheet(Stylesheet)

        self.pacerValueppm_Label = QtWidgets.QLabel(self.pacerPage)
        self.pacerValueppm_Label.setGeometry(QtCore.QRect(pantalla_config.pacerValueppm_CoordX1,
                                                        pantalla_config.pacerValueppm_CoordY1,
                                                        pantalla_config.pacerValueppm_HorizSize,
                                                        pantalla_config.pacerValueppm_VertSize))
        self.pacerValueppm_Label.setObjectName("pacerValueppm_Label")
        self.pacerValueppm_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.pacerValueppm_Label.setStyleSheet(Stylesheet)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Piplup"))
        self.DEFIB_pushButton.setText(_translate('Form', '1 DEFIB'))
        self.Charge_pushButton.setText(_translate('Form','2 CHARGE '))
        self.Shock_pushButton.setText(_translate('Form','3 SHOCK'))
        self.DEA_pushButton.setText(_translate('Form','DEA'))
        self.SYNC_pushButton.setText(_translate('Form','SYNC'))
        self.DISCHARGE_pushButton.setText(_translate('Form','DISCHARGE'))
        self.confirmMenu_pushButton.setText(_translate('Form','CONFIRM'))
        self.returnMenu_pushButton.setText(_translate('Form','RETURN'))
        self.paniMenu_pushButton.setText(_translate('Form','PANI'))
        self.alarmMenu_pushButton.setText(_translate('Form','ALARM\nSUSPEND'))
        self.CPRMenu_pushButton.setText(_translate('Form','CPR'))
        self.sizeMenu_pushButton.setText(_translate('Form','SIZE'))
        self.LEADMenu_pushButton.setText(_translate('Form','LEAD'))
        self.energySelectLabel_pushButton.setText(_translate('Form','Energy Select'))
        self.MARCPLabel_pushButton.setText(_translate('Form','P\nA\nC\nE\nR'))
        self.mALabel_pushButton.setText(_translate('Form','mA'))
        self.PPMLabel_pushButton.setText(_translate('Form','PPM'))
        self.pacerOutput_Label.setText(_translate('Form','PACER \n OUTPUT'))
        self.pacerRate_Label.setText(_translate('Form','PACER \n RATE'))
        self.version_Label.setText(_translate('Form','Version 0.00'))
        self.simulationTimeValue_pushButton.setText(_translate('Form','00:00:00'))
        self.simulationTimeLabel_Label.setText(_translate('Form','Simulation Time'))
        self.heartRateLabel_pushButton.setText(_translate('Form','Heart Rate'))
        self.heartRateValue_Label.setText(_translate('Form','- - -'))
        self.heartRateUnidades_Label.setText(_translate('Form','lpm'))
        self.tempLabel_pushButton.setText(_translate('Form','TEMP'))
        self.tempValue_Label.setText(_translate('Form','- - -'))
        self.tempUnidades_Label.setText(_translate('Form','C'))
        self.SpO2Label_pushButton.setText(_translate('Form','SpO2 Level'))
        self.SpO2Value_Label.setText(_translate('Form','- - -'))
        self.SpO2Unidades_Label.setText(_translate('Form','%'))
        self.pressureLabel_pushButton.setText(_translate('Form','Pressure'))
        self.pressureValue_Label.setText(_translate('Form','- - -'))
        self.pressureUnidades_Label.setText(_translate('Form','mmHg'))
        self.FRLabel_pushButton.setText(_translate('Form','FR'))
        self.FRValue_Label.setText(_translate('Form','- - -'))
        self.FRUnidades_Label.setText(_translate('Form','/min'))
        self.CO2Label_pushButton.setText(_translate('Form','CO2 Level'))
        self.CO2Value_Label.setText(_translate('Form','- - -'))
        self.CO2Unidades_Label.setText(_translate('Form','mmHg'))
        self.CRPRateLabel_Label.setText(_translate('Form','Rate (cpm)'))
        self.CRPRateValue_Label.setText(_translate('Form','110'))
        self.CRPTimeLabel_Label.setText(_translate('Form','CPR Time'))
        self.CRPTimeValue_Label.setText(_translate('Form','00:00'))
        self.CRPFCTLabel_Label.setText(_translate('Form','FCT'))
        self.CRPFCTValue_Label.setText(_translate('Form','100%'))
        self.defibLabel_pushButton.setText(_translate('Form','DEFIB 0 J SEL\nBIFASICO'))
        self.pacerLabelText_Label.setText(_translate('Form',"PACEMAKER"))
        self.pacerValuemA_Label.setText(_translate('Form',"18 mA"))
        self.pacerValueppm_Label.setText(_translate('Form',"70 ppm"))


        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    Form = QtWidgets.QWidget()
    ui = Ui_window()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
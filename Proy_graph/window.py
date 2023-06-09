### Graficas de deslegue continua  
# Autor: Alan 
# Informacion 
# https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg 
import sys 
from StylesheetFormat import Stylesheet
import pantalla_config
from samples import UPRoundTriangle, RoundButton, DOWNRoundTriangle



class Ui_window(object):
    def setupUi(self, Form):
        ### Inicio de Configuracion de los Widgets
        Form.setObjectName("Pokemon")
        Form.resize(pantalla_config.Horiz_size, pantalla_config.Vert_size)

            # Graph
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
        painter.drawRoundedRect(3, 3,pantalla_config.roundRectGrah_HorizSize, pantalla_config.roundRectGrah_VertSize, 20, 20)
        painter.end()

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

        ## Qpaint Round Rects
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
        painter.drawRoundedRect(3, 3,pantalla_config.roundRectDCS_HorizSize, pantalla_config.roundRectDCS_VertSize, 20, 20)
        painter.end()
            # MCP
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
        painter.drawRoundedRect(3, 3,pantalla_config.roundRectMCP_HorizSize, pantalla_config.roundRectMCP_VertSize, 20, 20)
        painter.end()
        
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
        
        ### Button Play, Pause, Stop, Question
            #Button
        Play_icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Play_icon.svg"))
        self.play_RoundButton = RoundButton(Form)
        #self.play_RoundButton.setButtonIcon(Play_icon)
        """self.play_RoundButton.setIcon(Play_icon)
        play_buttonSize = self.play_RoundButton.size()
        self.play_RoundButton.setIconSize(QtCore.QSize(play_buttonSize.width(), play_buttonSize.height()))"""
        self.play_RoundButton.setGeometry(QtCore.QRect(pantalla_config.play_CoordX1,
                                                    pantalla_config.play_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.play_RoundButton.setObjectName("play_RoundButton")
        
        self.pause_RoundButton = RoundButton(Form)
        Pause_icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Pause_icon.svg"))
        self.pause_RoundButton.setIcon(Pause_icon)
        pause_buttonSize = self.pause_RoundButton.size()
        self.pause_RoundButton.setIconSize(QtCore.QSize(pause_buttonSize.width(), pause_buttonSize.height()))
        self.pause_RoundButton.setGeometry(QtCore.QRect(pantalla_config.pause_CoordX1,
                                                    pantalla_config.pause_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.pause_RoundButton.setObjectName("pause_RoundButton")
        
        self.stop_RoundButton = RoundButton(Form)
        Stop_icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Stop_icon.svg"))
        self.stop_RoundButton.setIcon(Stop_icon)
        stop_buttonSize = self.stop_RoundButton.size()
        self.stop_RoundButton.setIconSize(QtCore.QSize(stop_buttonSize.width(), stop_buttonSize.height()))
        self.stop_RoundButton.setGeometry(QtCore.QRect(pantalla_config.stop_CoordX1,
                                                    pantalla_config.stop_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.stop_RoundButton.setObjectName("stop_RoundButton")
        
        self.question_RoundButton = RoundButton(Form)
        Quiestion_icon = QtGui.QIcon(QtGui.QPixmap("PyQt_Images/Question_icon.svg"))
        self.question_RoundButton.setIcon( Quiestion_icon )
        question_buttonSize = self.question_RoundButton.size()
        self.question_RoundButton.setIconSize(QtCore.QSize(question_buttonSize.width(), question_buttonSize.height()))
        self.question_RoundButton.setGeometry(QtCore.QRect(pantalla_config.question_CoordX1,
                                                    pantalla_config.question_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.question_RoundButton.setObjectName("question_RoundButton")
        
        self.OnOff_RoundButton = RoundButton(Form)
        #OnOff_buttonSize = self.OnOff_RoundButton.size()
        #self.OnOff_RoundButton.setIconSize(QtCore.QSize(OnOff_buttonSize.width(), OnOff_buttonSize.height()))
        self.OnOff_RoundButton.setGeometry(QtCore.QRect(pantalla_config.OnOff_CoordX1,
                                                    pantalla_config.OnOff_CoordY1,
                                                    pantalla_config.PPSQ_RoundButtonSize,
                                                    pantalla_config.PPSQ_RoundButtonSize))
        self.OnOff_RoundButton.setObjectName("OnOff_RoundButton")

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

        self.config_pushButton = RoundButton(Form)
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
        self.KabSinLogo_horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.KabSinLogo_horizontalLayoutWidget.setGeometry(QtCore.QRect(pantalla_config.KabSimLogo_CoordX1,
                                                                        pantalla_config.KabSimLogo_CoordY,
                                                                        pantalla_config.KabSimLogo_HorizSize,
                                                                        pantalla_config.KabSimLogo_VertSize))
        self.KabSinLogo_horizontalLayoutWidget.setObjectName("KabSinLogo_horizontalLayoutWidget")
        self.KabSinLogo_horizontalLayout = QtWidgets.QHBoxLayout(self.KabSinLogo_horizontalLayoutWidget)
        self.KabSinLogo_horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.KabSinLogo_horizontalLayout.setObjectName("KabSinLogo_horizontalLayout")

        self.KabSimLogo_Scene = QtWidgets.QGraphicsScene(0, 0, self.KabSinLogo_horizontalLayoutWidget.width(), self.KabSinLogo_horizontalLayoutWidget.height())
        self.KabSimLogo_Path = "PyQt_Images/KabSim_icon.svg"
        self.KabSimLogo_Image = QtGui.QPixmap(self.KabSimLogo_Path)
        self.KabSimLogo_pixmapitem = self.KabSimLogo_Scene.addPixmap(self.KabSimLogo_Image.scaled(self.KabSimLogo_Scene.sceneRect().size().toSize()))
        self.KabSimLogo_pixmapitem.setPos(0,0)
        
        self.KabSimLogo_view = QtWidgets.QGraphicsView(self.KabSimLogo_Scene)
        self.KabSimLogo_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.KabSimLogo_view.setStyleSheet("border: none;background: none;")
        self.KabSinLogo_horizontalLayout.addWidget(self.KabSimLogo_view)
        
        self.heartRateLabel_pushButton = QtWidgets.QPushButton(Form)
        self.heartRateLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.heartRateLabel_CoordX1,
                                                            pantalla_config.heartRateLabel_CoordY,
                                                            pantalla_config.heartRateLabel_HorizSize,
                                                            pantalla_config.heartRateLabel_VertSize))
        self.heartRateLabel_pushButton.setObjectName("heartRateLabel_pushButton")
        self.heartRateLabel_pushButton.setStyleSheet(Stylesheet)

        self.tempLabel_pushButton = QtWidgets.QPushButton(Form)
        self.tempLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.tempLabel_CoordX1,
                                                        pantalla_config.tempLabel_CoordY,
                                                        pantalla_config.tempLabel_HorizSize,
                                                        pantalla_config.tempLabel_VertSize))
        self.tempLabel_pushButton.setObjectName("tempLabel_pushButton")
        self.tempLabel_pushButton.setStyleSheet(Stylesheet)

        self.SpO2Label_pushButton = QtWidgets.QPushButton(Form)
        self.SpO2Label_pushButton.setGeometry(QtCore.QRect(pantalla_config.SpO2Label_CoordX1,
                                                    pantalla_config.SpO2Label_CoordY,
                                                    pantalla_config.SpO2Label_HorizSize,
                                                    pantalla_config.SpO2Label_VertSize))
        self.SpO2Label_pushButton.setObjectName("SpO2Label_pushButton")
        self.SpO2Label_pushButton.setStyleSheet(Stylesheet)
        
        self.pressureLabel_pushButton = QtWidgets.QPushButton(Form)
        self.pressureLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.pressureLabel_CoordX1,
                                                        pantalla_config.pressureLabel_CoordY,
                                                        pantalla_config.pressureLabel_HorizSize,
                                                        pantalla_config.pressureLabel_VertSize))
        self.pressureLabel_pushButton.setObjectName("pressureLabel_pushButton")
        self.pressureLabel_pushButton.setStyleSheet(Stylesheet)

        self.FRLabel_pushButton = QtWidgets.QPushButton(Form)
        self.FRLabel_pushButton.setGeometry(QtCore.QRect(pantalla_config.FRLabel_CoordX1,
                                                    pantalla_config.FRLabel_CoordY,
                                                    pantalla_config.FRLabel_HorizSize,
                                                    pantalla_config.FRLabel_VertSize))
        self.FRLabel_pushButton.setObjectName("FRLabel_pushButton")
        self.FRLabel_pushButton.setStyleSheet(Stylesheet)

        self.CO2Label_pushButton = QtWidgets.QPushButton(Form)
        self.CO2Label_pushButton.setGeometry(QtCore.QRect(pantalla_config.CO2Label_CoordX1,
                                                        pantalla_config.CO2Label_CoordY,
                                                        pantalla_config.CO2Label_HorizSize,
                                                        pantalla_config.CO2Label_VertSize))
        self.CO2Label_pushButton.setObjectName("CO2Label_pushButton")
        self.CO2Label_pushButton.setStyleSheet(Stylesheet)
        



        self.retranslateUi(Form)
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Piplup"))
        self.DEFIB_pushButton.setText(_translate('Form', '1 DEFIB'))
        self.Charge_pushButton.setText(_translate('Form','2 CHARGE '))
        self.Shock_pushButton.setText(_translate('Form','3 SHOCK'))
        self.DEA_pushButton.setText(_translate('Form','DEA'))
        self.SYNC_pushButton.setText(_translate('Form','SYNC'))
        self.confirmMenu_pushButton.setText(_translate('Form','CONFIRM'))
        self.returnMenu_pushButton.setText(_translate('Form','RETURN'))
        self.alarmMenu_pushButton.setText(_translate('Form','ALARM\nSUSPEND'))
        self.CPRMenu_pushButton.setText(_translate('Form','CRP'))
        self.sizeMenu_pushButton.setText(_translate('Form','SIZE'))
        self.LEADMenu_pushButton.setText(_translate('Form','LEAD'))
        self.energySelectLabel_pushButton.setText(_translate('Form','Energy\nSelect'))
        self.MARCPLabel_pushButton.setText(_translate('Form','MARCP'))
        self.mALabel_pushButton.setText(_translate('Form','mA'))
        self.PPMLabel_pushButton.setText(_translate('Form','PPM'))
        self.pacerOutput_Label.setText(_translate('Form','PACER \n OUTPUT'))
        self.pacerRate_Label.setText(_translate('Form','PACER \n RATE'))
        self.version_Label.setText(_translate('Form','Version 0.00'))
        self.heartRateLabel_pushButton.setText(_translate('Form','Heart Rate'))
        self.tempLabel_pushButton.setText(_translate('Form','TEMP'))
        self.SpO2Label_pushButton.setText(_translate('Form','SpO2 Level'))
        self.pressureLabel_pushButton.setText(_translate('Form','Pressure'))
        self.FRLabel_pushButton.setText(_translate('Form','FR'))
        self.CO2Label_pushButton.setText(_translate('Form','CO2 Level'))


        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    Form = QtWidgets.QWidget()
    ui = Ui_window()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
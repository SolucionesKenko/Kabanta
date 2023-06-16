from PyQt5 import QtWidgets #import QApplication, QPushButton
from PyQt5 import QtGui #import QPainter, QColor
from PyQt5 import QtCore # import Qt
import pantalla_config
import sys

class UPRoundTriangle(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(UPRoundTriangle, self).__init__(parent)
        self.setFixedSize(pantalla_config.Triangle_RoundButtonSize,pantalla_config.Triangle_RoundButtonSize)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Set triangle coordinates

        triangle = QtGui.QPolygonF()
        Middle = round(pantalla_config.Triangle_RoundButtonSize/2)
        triangle.append(QtCore.QPointF(Middle, 0))
        triangle.append(QtCore.QPointF(0, pantalla_config.Triangle_RoundButtonSize))
        triangle.append(QtCore.QPointF(pantalla_config.Triangle_RoundButtonSize, pantalla_config.Triangle_RoundButtonSize))

        # Draw the rounded button
        painter.setBrush(QtGui.QColor(84,84,84))  # Replace with your desired color
        painter.drawPolygon(triangle)
    
    def sizeHint(self):
        return self.minimumSizeHint()

class DOWNRoundTriangle(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(DOWNRoundTriangle, self).__init__(parent)
        self.setFixedSize(pantalla_config.Triangle_RoundButtonSize,pantalla_config.Triangle_RoundButtonSize)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Set triangle coordinates

        triangle = QtGui.QPolygonF()
        Middle = round(pantalla_config.Triangle_RoundButtonSize/2)
        triangle.append(QtCore.QPointF(Middle, pantalla_config.Triangle_RoundButtonSize))
        triangle.append(QtCore.QPointF(pantalla_config.Triangle_RoundButtonSize, 0))
        triangle.append(QtCore.QPointF(0, 0))

        # Draw the rounded button
        painter.setBrush(QtGui.QColor(84,84,84))  # Replace with your desired color
        painter.drawPolygon(triangle)
    
    def sizeHint(self):
        return self.minimumSizeHint()

    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    button = UPRoundTriangle()
    button.show()
    sys.exit(app.exec_())

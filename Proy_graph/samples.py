from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
import pantalla_config
import sys

class RoundButton(QPushButton):
    def __init__(self, parent=None):
        super(RoundButton, self).__init__(parent)
        self.setFixedSize(pantalla_config.PPSQ_RoundButtonSize, pantalla_config.PPSQ_RoundButtonSize)  # Set the fixed size of the button to make it round

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the button background color
        painter.setBrush(QColor(255, 0, 0))  # Replace with your desired color

        # Draw the rounded button
        painter.drawEllipse(0, 0, self.width(), self.height())

    def sizeHint(self):
        return self.minimumSizeHint()
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    button = RoundButton()
    button.show()
    sys.exit(app.exec_())

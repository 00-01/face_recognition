import sys
import cv2
# import Login
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


def add_new(self):
    widget.addWidget(Add_New())
    widget.setCurrentIndex(widget.currentIndex() + 1)


class Add_New(QDialog):
    def __init__(self):
        super(Add_New, self).__init__()
        loadUi('./add_new.ui', self)

        self.add_new.clicked.connect(self.captureFrame)

    def captureFrame(self, event, x, y, flags, frame):
        # if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.imwrite('test.png', frame)
        print('captured')


# app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.show()
# sys.exit(app.exec_())
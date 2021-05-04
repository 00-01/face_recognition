import cv2
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from page import Page
from save import Save


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('ui/login.ui', self)

        self.loginButton.clicked.connect(self.login)
        self.signupButton.clicked.connect(self.create)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)

    def login(self):
        from face_rec import Face_Recognition
        id = self.ID.text()
        pw = self.PW.text()
        print(f'{id} has logged in')
        self.widget.addWidget(Face_Recognition())
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
    #
    # def save(self):
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     self.take_photo.stop()
    #
    #     widget.addWidget(self.save)
    #     widget.setCurrentIndex(widget.currentIndex() + 1)

    def create(self):
        from signup import Signup
        self.widget.addWidget(Signup())
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)


# if __name__ == '__main__':
#     main = Main()
#     widget = Page()
#     widget.addWidget(main)
#     widget.show()
#     # sys.exit(app.exec_())

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.setFixedHeight(1280)
widget.setFixedWidth(800)
widget.setWindowFlag(Qt.WindowStaysOnTopHint)
sys.exit(app.exec_())

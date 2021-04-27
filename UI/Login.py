import sys
import cv2
from main import Face_Recognition
# from old_main import Face_Recognition
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('./login.ui', self)

        self.loginButton.clicked.connect(self.login)
        self.signupButton.clicked.connect(self.create)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)

    def login(self):
        id = self.ID.text()
        pw = self.PW.text()
        print(f'{id} has logged in')
        widget.addWidget(Face_Recognition())
        widget.setCurrentIndex(widget.currentIndex()+1)

    def create(self):
        widget.addWidget(Signup())
        widget.setCurrentIndex(widget.currentIndex()+1)

class Signup(QDialog):
    def __init__(self):
        super(Signup, self).__init__()
        loadUi('./signup.ui', self)
        self.signupButton.clicked.connect(self.createId)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PW_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def createId(self):
        id = self.ID.text()
        if self.PW.text() == self.PW_2.text():
            pw = self.PW.text()
            print(f'create ID: {id} success!')

            widget.addWidget(Login())
            widget.setCurrentIndex(widget.currentIndex()+1)


# class Add_New(QDialog):
#     def __init__(self):
#         super(Add_New, self).__init__()
#         loadUi('./add_new.ui', self)
#
#         self.add_new.clicked.connect(self.captureFrame)
#
#     def captureFrame(self, event, x, y, flags, frame):
#         # if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.imwrite('test.png', frame)
#         print('captured')


app = QApplication(sys.argv)
login = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.setFixedHeight(1280)
widget.setFixedWidth(800)
widget.show()
sys.exit(app.exec_())

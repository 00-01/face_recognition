from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class Signup(QDialog):
    def __init__(self):
        super(Signup, self).__init__()
        loadUi('ui/signup.ui', self)
        self.signupButton.clicked.connect(self.createId)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PW_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def createId(self):
        id = self.ID.text()
        if self.PW.text() == self.PW_2.text():
            pw = self.PW.text()
            print(f'create ID: {id} success!')

            # self.widget = Page()
            self.widget = QtWidgets.QWidget()
            self.main = Main()
            self.main.setupUi(self.widget)
            self.widget.show()

            self.widget.addWidget(self.widget)
            self.widget.setCurrentIndex(self.widget.currentIndex()+1)


# class Ui_Dialog(QDialog):
#     def __init__(self):
#         super(Ui_Dialog, self).__init__()
#         loadUi("mainwindow.ui", self)
#
#         self.runButton.clicked.connect(self.runSlot)
#
#         self._new_window = None
#         self.Videocapture_ = None
#
#     def refreshAll(self):
#         """
#         Set the text of lineEdit once it's valid
#         """
#         self.Videocapture_ = "0"
#
#     @pyqtSlot()
#     def runSlot(self):
#         """
#         Called when the user presses the Run button
#         """
#         print("Clicked Run")
#         self.refreshAll()
#         print(self.Videocapture_)
#         ui.hide()  # hide the main window
#         self.outputWindow_()  # Create and open new output window
#
#     def outputWindow_(self):
#         """
#         Created new window for vidual output of the video in GUI
#         """
#         self._new_window = Ui_OutputDialog()
#         self._new_window.show()
#         self._new_window.startVideo(self.Videocapture_)
#         print("Video Played")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ui = Ui_Dialog()
#     ui.show()
#     sys.exit(app.exec_())

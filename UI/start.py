import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from old_main import Ui_OutputDialog


class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("./login.ui", self)
        self.loginButton.clicked.connect(self.runSlot)  # wait for 'start' click
        self._new_window = Ui_OutputDialog()

    @pyqtSlot()
    def runSlot(self):
        ui.hide()  # hide start window
        self._new_window.startVideo(0)  # camera number
        self._new_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())

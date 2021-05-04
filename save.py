from time import time
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

# cap = cv2.VideoCapture(0)


class Save(QDialog):
    def __init__(self):
        super(Save, self).__init__()
        loadUi('ui/save.ui', self)
        self.save.clicked.connect(self.captureFrame)

        self.take_photo = Take_photo()
        self.take_photo.start()
        self.take_photo.ImageUpdate.connect(self.ImageUpdateSlot)

    def captureFrame(self, event, x, y, flags, frame):
        cv2.imwrite('test.png', frame)
        print('captured')

    def ImageUpdateSlot(self, Image):
        self.imgLabel.setPixmap(QPixmap.fromImage(Image))
        self.imgLabel.setScaledContents(True)

class Take_photo(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            s = time()
            ret, frame = cap.read(0)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ImageUpdate.emit(img)
        # calculate fps
        #     seconds = time() - s
        #     fps = 1 / seconds
        #     fps = ("%.2f" % fps)
            # print(f"fps : {fps}", '\n')

    def stop(self):
        self.ThreadActive = False
        self.quit()
import cv2
from time import time
import face_recognition
import numpy as np
from save import Save
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from db import access_db

_, _, col, error_col = access_db()
n = list(col.find({}))
names = [i['name'] for i in n]
id = [j['id'] for j in n]


class Face_Recognition(QDialog):
    def __init__(self):
        super(Face_Recognition, self).__init__()
        loadUi("ui/face_rec.ui", self)
        self.startVideo()
        self.widget = QtWidgets.QStackedWidget()

        self.add.clicked.connect(self.save)


    @pyqtSlot()
    def startVideo(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)  # Create Timer
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(0)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame):
        s = time()
        threshold = 0.35
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "------"
            matches = face_recognition.compare_faces(id, face_encoding, tolerance=threshold)
            face_distances = face_recognition.face_distance(id, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = names[best_match_index]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left - 1, bottom + 24), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), 1)
            print('name : ', name)
        # calculate fps
            seconds = time() - s
            fps = 1 / seconds
            fps = ("%.2f" % fps)
            print(f"fps : {fps}", '\n')
        # output img
            qformat = QImage.Format_Indexed8
            if len(frame.shape) == 3:
                if frame.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
            outImage = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], qformat)
            outImage = outImage.rgbSwapped()

            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

    def update_frame(self):
        ret, self.image = self.cap.read(0)  # grayscale
        self.image = cv2.flip(self.image, 1)
        self.face_rec_(self.image)

    def save(self):
        self.cap.release()
        # cv2.destroyAllWindows()
        self.widget.addWidget(Save())
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

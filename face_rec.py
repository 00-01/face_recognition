from time import time
import cv2
import face_recognition
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from db import access_db
# from page import Page
from save import Save

_, _, col, error_col = access_db()
n = list(col.find({}))
names = [i['name'] for i in n]
id = [j['id'] for j in n]


cap = cv2.VideoCapture(0)

class Face_Recognition(QDialog):
    def __init__(self):
        super(Face_Recognition, self).__init__()
        loadUi("ui/face_rec.ui", self)
        self.add.clicked.connect(self.add_new_id)

        self.run = Run_Camera()
        self.run.start()
        self.run.ImageUpdate.connect(self.ImageUpdateSlot)

    def ImageUpdateSlot(self, Image):
        self.imgLabel.setPixmap(QPixmap.fromImage(Image))
        self.imgLabel.setScaledContents(True)

    def add_new_id(self):
        cap.release()
        cv2.destroyAllWindows()
        self.run.stop()

        self.widget = QtWidgets.QWidget()
        save = Save()
        self.save.setupUi(self.widget)
        self.widget.show()

        self.widget.addWidget(self.widget)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

class Run_Camera(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            s = time()
            ret, frame = cap.read(0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            threshold = 0.35
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "- - -"
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
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ImageUpdate.emit(img)

    def stop(self):
        self.ThreadActive = False
        self.quit()

# if __name__ == "__main__":
#     App = QApplication(sys.argv)
#     Root = MainWindow()
#     Root.show()
#     sys.exit(App.exec())
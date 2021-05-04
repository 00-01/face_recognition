import sys
import cv2
from time import time
import face_recognition
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from db import access_db


class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('ui/login.ui', self)

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
        loadUi('ui/signup.ui', self)
        self.signupButton.clicked.connect(self.createId)
        self.PW.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PW_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def createId(self):
        id = self.ID.text()
        if self.PW.text() == self.PW_2.text():
            pw = self.PW.text()
            print(f'create ID: {id} success!')

            widget.addWidget(Main())
            widget.setCurrentIndex(widget.currentIndex()+1)


client, db, col, error_col = access_db()
n = list(col.find({}))
names = [i['name'] for i in n]
id = [j['id'] for j in n]
cam_num = 0
cap = cv2.VideoCapture(cam_num)
path = 'new/'
ext = '.jpg'
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
        # cap.release()
        # cv2.destroyAllWindows()
        self.run.stop()

        widget.addWidget(Save())
        widget.setCurrentIndex(widget.currentIndex()+1)

class Run_Camera(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            s = time()
            ret, frame = cap.read(0)
            # frame = frame[:, :, ::-1]
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


class Save(QDialog):
    def __init__(self):
        super(Save, self).__init__()
        loadUi('ui/save.ui', self)
        self.save.clicked.connect(self.capture)
        self.retrn.clicked.connect(self.face_rec)

        self.take_photo = Take_photo()
        self.take_photo.start()
        self.take_photo.ImageUpdate.connect(self.ImageUpdateSlot)

    def capture(self):
        screenshot = QScreen.grabWindow(app.primaryScreen(), widget.winId(), 0, 0, 800, 1080)

        msg = QMessageBox()
        msg.setWindowFlag(Qt.WindowStaysOnTopHint)
        msg.setIconPixmap(QPixmap(screenshot))
        msg.setText('저장 하시겠습니까?')
        msg.setStandardButtons(QMessageBox.No|QMessageBox.Yes)
        x = msg.exec_()

        if x == QMessageBox.Yes:
            name = self.name.text()
            captured_img = path + name + ext
            screenshot.save(captured_img)
            print('img saved to dir : ', name)
            try:
                id = face_recognition.face_encodings(face_recognition.load_image_file(captured_img), model='large')[0]
                data = {'name': name, 'id': id.tolist()}
                col.insert_one(data)
                print('face_id saved to db : ', name)
            except IndexError:
                error_col.insert_one({'name': name})
                print('warning! face not detected! : ', name)
            # client.close()
            print('finished')
        else: pass

    def face_rec(self):
        widget.addWidget(Face_Recognition())
        widget.setCurrentIndex(widget.currentIndex()+1)

    def ImageUpdateSlot(self, Image):
        self.imgLabel.setPixmap(QPixmap.fromImage(Image))
        self.imgLabel.setScaledContents(True)

class Take_photo(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        # cap = cv2.VideoCapture(cam_num)
        while self.ThreadActive:
            ret, frame = cap.read(0)
            # # frame = frame[:, :, ::-1]  # BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ImageUpdate.emit(img)
            # if len(key) > 0:
            #     cv2.imwrite('test.png', frame)

    # def stop(self):
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     self.ThreadActive = False
    #     self.quit()


app = QApplication(sys.argv)
main = Main()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main)
widget.setFixedHeight(1280)
widget.setFixedWidth(800)
widget.setWindowFlag(Qt.WindowStaysOnTopHint)
widget.show()
sys.exit(app.exec_())

import csv
import datetime
import os
import cv2
import face_recognition
import numpy as np
from time import time
from db import access_db
# from Add_New import add_new
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer, QDate
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi


threshold = 0.3
client, db, col, error_col = access_db()
n = list(col.find({}))

class Face_Recognition(QDialog):
    def __init__(self):
        super(Face_Recognition, self).__init__()
        loadUi("./main.ui", self)
        # self.add.clicked.connect(add_new())

        self.startVideo(0)
    #datetime
        now = QDate.currentDate()
        current_date = now.toString('yyyy MMMM dd ddd')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)

        self.image = None

    @pyqtSlot()
    def startVideo(self, camera_name):
        self.capture = cv2.VideoCapture(camera_name)

        self.timer = QTimer(self)  # Create Timer
        path = 'ImagesAttendance'
        if not os.path.exists(path):
            os.mkdir(path)
    # known face encoding and known face name list
        images = []
        self.class_names = [i['name'] for i in n]
        self.encode_list = [j['id'] for j in n]
        self.TimeList1 = []
        self.TimeList2 = []
        attendance_list = os.listdir(path)

        # print(attendance_list)
        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # csv
        def mark_attendance(name):
            if self.ClockInButton.isChecked():
                self.ClockInButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                    if (name != 'unknown'):
                        buttonReply = QMessageBox.question(self, 'Welcome ' + name, 'Are you Clocking In?' ,
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:

                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            f.writelines(f'\n{name},{date_time_string},Clock In')
                            self.ClockInButton.setChecked(False)

                            self.NameLabel.setText(name)
                            self.StatusLabel.setText('Clocked In')
                            self.HoursLabel.setText('Measuring')
                            self.MinLabel.setText('')

                            #self.CalculateElapse(name)
                            #print('Yes clicked and detected')
                            self.Time1 = datetime.datetime.now()
                            #print(self.Time1)
                            self.ClockInButton.setEnabled(True)
                        else:
                            print('Not clicked.')
                            self.ClockInButton.setEnabled(True)
            elif self.ClockOutButton.isChecked():
                self.ClockOutButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                    if (name != 'unknown'):
                        buttonReply = QMessageBox.question(self, 'Cheers ' + name, 'Are you Clocking Out?',
                                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            f.writelines(f'\n{name},{date_time_string},Clock Out')
                            self.ClockOutButton.setChecked(False)

                            self.NameLabel.setText(name)
                            self.StatusLabel.setText('Clocked Out')
                            self.Time2 = datetime.datetime.now()
                            #print(self.Time2)

                            # self.ElapseList(name)
                            self.TimeList2.append(datetime.datetime.now())
                            CheckInTime = self.TimeList1[-1]
                            CheckOutTime = self.TimeList2[-1]
                            self.ElapseHours = (CheckOutTime - CheckInTime)
                            self.MinLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60)%60) + 'm')
                            self.HoursLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60**2)) + 'h')
                            self.ClockOutButton.setEnabled(True)
                        else:
                            print('Not clicked.')
                            self.ClockOutButton.setEnabled(True)

    # face recognition
        s = time()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "-unregistered-"
            matches = face_recognition.compare_faces(encode_list_known, face_encoding, tolerance=threshold)
            face_distances = face_recognition.face_distance(encode_list_known, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = class_names[best_match_index]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left - 1, bottom + 24), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), 1)
            print(name)
            mark_attendance(name)
        # calculate fps
            seconds = time() - s
            fps = 1 / seconds
            print(f"Sec per frame : {seconds}")
            print(f"frame per sec : {fps}", '\n')

        return frame

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def ElapseList(self,name):
        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Clock In':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'Clock Out':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time2 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
                                self.TimeList2.append(Time2)
                                #print(Time2)

    def update_frame(self):
        ret, self.image = self.capture.read()
        # self.image = cv2.flip(self.image, 1)
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

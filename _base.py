import cv2
import face_recognition
import numpy as np
from db import access_db
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer, QDate
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from datetime import datetime
from time import time
start = datetime.now()


# get data from dbms
_, _, col, error_col = access_db()
n = list(col.find({}))
code = [i['name'] for i in n]
id = [j['id'] for j in n]

threashold = 0.35
window_name = 'face_detection'
cap = cv2.VideoCapture(0)
while True:
    s = time()
    ret, frame = cap.read(0)  # read grayscale
    frame = cv2.flip(frame, 1)  # horizontal flip
    # rgb_frame = frame[:, :, ::-1]  # BGR to RGB

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "-unregistered-"
        matches = face_recognition.compare_faces(id, face_encoding, tolerance=threashold)
        face_distances = face_recognition.face_distance(id, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = code[best_match_index]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left - 1, bottom + 24), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), 1)
        print(name)
    # calculate fps
        seconds = time() - s
        fps = 1 / seconds
        print(f"Sec per frame : {seconds}")
        print(f"frame per sec : {fps}", '\n')
# mouse click to save frame
#     cv2.setMouseCallback(window_name, new_face.captureFrame, frame)
    cv2.imshow(window_name, frame)
    if cv2.waitKey(1) & 0xFF == 27: break

print('total run time : ', datetime.now() - start)
cap.release()
cv2.destroyAllWindows()

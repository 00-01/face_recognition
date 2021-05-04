# import sys
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication
#
# class Page():
#     def __init__(self):
#         self.widget = QtWidgets.QStackedWidget()
#         self.widget.setFixedHeight(1280)
#         self.widget.setFixedWidth(800)
#         self.widget.setWindowFlag(Qt.WindowStaysOnTopHint)
#         self.app = QApplication(sys.argv)
#         sys.exit(self.app.exec_())


import cv2


index = 0
arr = []
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        arr.append(index)
    cap.release()
    index += 1

    print(arr)
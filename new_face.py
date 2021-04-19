from glob import glob
import cv2
import face_recognition
from db import access_db

client, db, col, error_col = access_db()
result = col.find()


def captureFrame(event,x,y,flags,frame):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.imwrite('test.png',frame)
        print('captured')




# try:
#     id = face_recognition.face_encodings(face_recognition.load_image_file(i), model='large')[0]
#     data = {'name': name, 'id': id.tolist()}
#     col.insert_one(data)
#     print(name)
# except IndexError:
#     error_col.insert_one({'name': name})
#     print('cannot add: ', name)
#
# client.close()
# print('new face saved')
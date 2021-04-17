import cv2
import face_recognition
import numpy as np
from db import access_db
import new_face
from datetime import datetime
start = datetime.now()


client, db, col = access_db()
result = col.find()

name = []
id = []
for i in result:
    name.append(i['name'])
    id.append(i['id'])

# def main():
frame_name = 'face_detection'
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    rgb_frame = frame[:, :, ::-1]

    # Find all faces and face encodings in video frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in video frame
    result = "-unregistered-"
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(id, face_encoding, tolerance=0.25)

        face_distances = face_recognition.face_distance(id, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]: result = name[best_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, result, (left - 1, bottom + 24),
                    cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), 1)
        print(result)

    cv2.setMouseCallback(frame_name, new_face.captureFrame, frame)
    cv2.imshow(frame_name, frame)
    if cv2.waitKey(1) & 0xFF == 27: break

print(datetime.now() - start)
cap.release()
cv2.destroyAllWindows()


# main()
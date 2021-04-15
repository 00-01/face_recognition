import encode
import face_recognition
import cv2
import numpy as np
from datetime import datetime
start_time = datetime.now()


encoded, name_list, error_list = encode.db('/home/a/Desktop/face_recognition/examples/img128/')

video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    # Find all faces and face encodings in video frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(encoded, face_encoding, tolerance=0.25)
        name = "-unregistered-"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = name_list[best_match_index]

    # face box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    # name
        # cv2.rectangle(frame, (left, bottom + 30), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left - 1, bottom + 24), font, 1.0, (255, 0, 0), 1)

    cv2.imshow('face detection', frame)
    if cv2.waitKey(1) == 27: break

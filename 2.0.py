import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime


video_capture = cv2.VideoCapture(0)

jobs_image = face_recognition.load_image_file("PROJECT CGV/cgv2/photos/jobs.jpg")
jobs_encoding = face_recognition.face_encodings(jobs_image)[0]

ratan_tata_image = face_recognition.load_image_file("PROJECT CGV/cgv2/photos/tata.jpg")
ratan_tata_encoding = face_recognition.face_encodings(ratan_tata_image)[0]

ravi_image = face_recognition.load_image_file("PROJECT CGV/cgv2/photos/ravi.jpg")
ravi_encoding = face_recognition.face_encodings(ravi_image)[0]

tesla_image = face_recognition.load_image_file("PROJECT CGV/cgv2/photos/tesla.jpeg")
tesla_encoding = face_recognition.face_encodings(tesla_image)[0]

virat_image = face_recognition.load_image_file("PROJECT CGV/cgv2/photos/virat.png")
virat_encoding = face_recognition.face_encodings(virat_image)[0]

known_face_encoding = [
    jobs_encoding,
    ratan_tata_encoding,
    tesla_encoding,
    ravi_encoding,
    virat_encoding
]

known_faces_names = [
    "jobs",
    "ratan_tata",
    "tesla",
    "ravi",
    "virat"
]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', 'w+', newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            if name in known_faces_names:
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name, current_time])
    cv2.imshow("attendance system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()


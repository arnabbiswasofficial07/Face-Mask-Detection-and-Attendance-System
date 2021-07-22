import numpy as np
import time
from attendance_list import *


def take_attendance():
    list_of_encoding_images = get_encodings()
    path = 'imagesAttendance'
    names_of_students = []
    directory_images = os.listdir(path)
    for img in directory_images:
        names_of_students.append(os.path.splitext(img)[0])

    name = ' '

    cap = cv2.VideoCapture(0)
    start_time = time.time()
    seconds = 15

    while True:
        success, img = cap.read()
        img_resize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

        faces_current_frame = face_recognition.face_locations(img_resize)
        encodings_current_frame = face_recognition.face_encodings(img_resize, faces_current_frame)

        for encode_face, face_loc in zip(encodings_current_frame, faces_current_frame):
            matches = face_recognition.compare_faces(list_of_encoding_images, encode_face)
            face_distance = face_recognition.face_distance(list_of_encoding_images, encode_face)
            match_index = np.argmin(face_distance)

            if matches[match_index]:
                name = names_of_students[match_index].upper()
                print(name)
                first_name_only = name.split()[0]
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, first_name_only, (x1 + 8, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('webcam', img)
        key = cv2.waitKey(1)

        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            print(name)
            break
    cv2.destroyAllWindows()

    return name

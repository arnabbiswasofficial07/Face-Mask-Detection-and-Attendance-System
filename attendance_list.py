import cv2
import os
import face_recognition


def get_encodings():
    path = 'imagesAttendance'
    images = []
    names_of_students = []
    directory_images = os.listdir(path)
    # print(directory_images)
    for img in directory_images:
        images.append(cv2.imread(f'{path}/{img}'))
        names_of_students.append(os.path.splitext(img)[0])
    # print(names_of_students)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode_img = face_recognition.face_encodings(img)[0]
                encodeList.append(encode_img)
            return encodeList
    list_of_encoding_images = findEncodings(images)

    return list_of_encoding_images
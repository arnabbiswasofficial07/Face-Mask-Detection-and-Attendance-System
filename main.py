import csv
import os
import sqlite3
import time
from datetime import datetime

import cv2
import face_recognition
import imutils
import numpy as np
from imutils.video import VideoStream
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

check = 0


def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                 (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()
    print(detections.shape)

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)


# load our serialized face detector model from disk
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model("mask_detector.model")

# initialize the video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()

# loop over the frames from the video stream
start_time = time.time()
seconds = 15
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # detect faces in the frame and determine if they are wearing a
    # face mask or not
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    # loop over the detected face locations and their corresponding
    # locations
    for (box, pred) in zip(locs, preds):
        # unpack the bounding box and predictions
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        # determine the class label and color we'll use to draw
        # the bounding box and text
        label = "Mask" if mask > withoutMask else "No Mask"
        if label == "Mask":
            check = 1

        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        # include the probability in the label
        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

        # display the label and bounding box rectangle on the output
        # frame
        cv2.putText(frame, label, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    # show the output frame
    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    # if key == ord("q"):
    #     break

    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > seconds:
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

print(check)

if check == 1:
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
            encodeimg = face_recognition.face_encodings(img)[0]
            encodeList.append(encodeimg)
        return encodeList


    def markAttendance(name):
        with open('Attendance.csv', 'r+') as f:
            data_list = f.readlines()
            # print(data_list)
            name_list = []
            only_name = name.split()
            full_name = only_name[0] + " " + only_name[1]
            reg_no = only_name[2]
            for data in data_list:
                entry = data.split(',')
                name_list.append(entry[1])
            if full_name not in name_list:
                time_now = datetime.now()
                datetime_string = time_now.strftime('%H:%M:%S')
                f.writelines(f'\n{reg_no},{full_name},{datetime_string}')


    list_of_encoding_images = findEncodings(images)
    # print(list_of_encoding_images)
    print(len(list_of_encoding_images))

    cap = cv2.VideoCapture(0)
    start_time = time.time()
    seconds = 10

    while True:
        success, img = cap.read()
        img_resize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

        faces_current_frame = face_recognition.face_locations(img_resize)
        encodings_current_frame = face_recognition.face_encodings(img_resize, faces_current_frame)

        for encode_face, face_loc in zip(encodings_current_frame, faces_current_frame):
            matches = face_recognition.compare_faces(list_of_encoding_images, encode_face)
            face_distance = face_recognition.face_distance(list_of_encoding_images, encode_face)
            # print(face_distance)
            match_index = np.argmin(face_distance)

            if matches[match_index]:
                name = names_of_students[match_index].upper()
                print(name)
                first_name_only = name.split()[0]
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, first_name_only, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)

        cv2.imshow('webcam', img)
        key = cv2.waitKey(1)

        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            print(name)
            break
    cv2.destroyAllWindows()
else:
    print("please wear the mask")

conn = sqlite3.connect("attendance.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists students
        (RegNo text,
        Name text,
        Time text)
''')

with open('Attendance.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['RegNo'], i['Name'], i['Time']) for i in dr]

cur.executemany("INSERT INTO students (RegNo, Name, Time) VALUES (?, ?, ?);", to_db)
conn.commit()
conn.close()

conn = sqlite3.connect("attendance.db")
c = conn.cursor()
c.execute("SELECT * FROM students")
print(c.fetchall())

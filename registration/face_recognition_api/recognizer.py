import numpy as np
from cv2 import cv2
import os
from fda.settings import MEDIA_ROOT as faceDataPath
from PIL import Image
import face_recognition

size = 4
haar_file = 'haarcascade_frontalface_default.xml'

datasets = faceDataPath

face_cascade = cv2.CascadeClassifier(haar_file)

(width, height) = (130, 100)

def captureImage(details):

    cv2.namedWindow("Test")
    camera_index = 0
    video = cv2.VideoCapture(camera_index)

    known_face_encodings = []
    known_face_names = []

    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # image_dir = os.path.join(base_dir, "static")
    # image_dir = os.path.join(image_dir, "profile_pics")

    # base_dir = os.getcwd()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # os.chdir("..")
    base_dir = os.getcwd()
    print("base dir is : " + base_dir)

    print(details['year'])
    print(details['shift'])

    image_dir = os.path.join(
        base_dir, 'face_data', 'Student_Images', details['year'], details['shift'])
    print("image dir is :" + image_dir)
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    names = []

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('jpg') or file.endswith('png'):
                path = os.path.join(root, file)
                img = face_recognition.load_image_file(path)
                label = file[:len(file)-4]
                img_encoding = face_recognition.face_encodings(img)[0]
                known_face_names.append(label)
                known_face_encodings.append(img_encoding)

    face_locations = []
    face_encodings = []

    while True:
        check, frame = video.read()
        # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2RGB)
        # faces = face_cascade.detectMultiScale(rgb_frame, 1.3, 4)
        small_frame = cv2.resize(frame, (width, height), fx = 0.5, fy = 0.5)
        rgb_small_frame = small_frame[:, :, :,:-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(
                known_face_encodings, np.array(face_encoding), tolerance=0.6)

            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)

            try:
                matches = face_recognition.compare_faces(
                    known_face_encodings, np.array(face_encoding), tolerance=0.6)

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_names.append(name)
                    if name not in names:
                        names.append(name)
            except:
                pass

        if len(face_names) == 0:
            for (top, right, bottom, left) in face_locations:
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)

                # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'Unknown', (left, top),
                            font, 0.8, (255, 255, 255), 1)
        else:
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 255, 0), 2)
                # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left, top),
                            font, 0.8, (255, 255, 255), 1)
                face_gray = gray[y:y + h, x:x + w]
                face = cv2.resize(face_gray, (width, height))
                cv2.imwrite('% s.png' % (details['rollnumber']), face)

        cv2.imshow("Face Recognition Panel", frame)

        if cv2.waitKey(1) == ord('s'):
            break

    video.release()
    cv2.destroyAllWindows()
    return face

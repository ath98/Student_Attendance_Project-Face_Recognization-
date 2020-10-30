from django.db.models.aggregates import Count
from pyttsx3 import init
from fd.settings import IMG_ROOT
import numpy as np
import cv2
import os
import keyboard
import pyttsx3

from .models import Attendance, Student


def MarkAttendance(details):
    presentRoll=[]
    attendance = Attendance()
    faceDetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    #datasets = IMG_ROOT + '/'+ +'/'+
    datasets = os.path.join(
        IMG_ROOT, details['lecture_year'], details['lecture_shift'])
    print(datasets)
    if not os.listdir(datasets) :
        print("Directory is empty")
    else:    
        print("Directory is not empty") 
    (images, lables, names, id) = ([], [], {}, 0)
    # for (subdir, dir, files) in os.walk(datasets):
    #     for subdir in dir:
    #         sub= os.path.join(datasets,subdir)
    #         for (subdir, dir, files) in os.walk(sub):
    #             for subdir in dir:
    #                 subIn = os.path.join(sub,subdir)
    #                 for (subdir, dir, files) in os.walk(subIn):
    #                     for subdir in files:
    #                         names[id] = subdir
    #                         path = os.path.join(subIn, subdir)
    #                         lable = id
    #                         images.append(cv2.imread(path, 0))
    #                         lables.append(int(lable))
    #                     id +=1
    for (sub,d, f) in os.walk(datasets):
        for di in d:
            names[id] = di
            subjectPath = os.path.join(datasets,di)
            for (subdir, dir, files) in os.walk(subjectPath):
                for subdir in files:
                    path = os.path.join(subjectPath,subdir)
                    print(path)
                    lable = id
                    images.append(cv2.imread(path, 0))
                    lables.append(int(lable))
                id += 1

    (images, lables) = [np.array(lis) for lis in [images, lables]]
    print(images)
    print(lables)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, lables)
    cam = cv2.VideoCapture(0)
    sampleNum = 0
    while keyboard.is_pressed('q') != True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=1
        )

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (130, 100))
            prediction = model.predict(face_resize)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if prediction[1] < 90:
                stdId = names[prediction[0]]       
                print(stdId)                         
                try:
                    if(presentRoll.index(stdId)):
                        print('exsists')
                        student = Student.objects.get(rollNumber=str(stdId))

                        if not student:
                            speaker = pyttsx3.init()
                            voice_rate = 150
                            speaker.setProperty('rate', voice_rate)
                            speaker.say('Student not found')
                            speaker.runAndWait()
                        else:
                            student_name = student.firstname
                            print(student_name)
                            say = student_name + ' attendance marked'
                            speaker = pyttsx3.init()
                            voice_rate = 150
                            speaker.setProperty('rate', voice_rate)
                            speaker.say(say)
                            speaker.runAndWait()
                except:
                    presentRoll.append(stdId)
                    student = Student.objects.get(rollNumber=str(stdId))

                    if not student:
                        speaker = pyttsx3.init()
                        voice_rate = 150
                        speaker.setProperty('rate', voice_rate)
                        speaker.say('Student not found')
                        speaker.runAndWait()
                    else:
                        student_name = student.firstname
                        print(student_name)
                        say = student_name + ' attendance marked'
                        speaker = pyttsx3.init()
                        voice_rate = 150
                        speaker.setProperty('rate', voice_rate)
                        speaker.say(say)
                        speaker.runAndWait()
                
                # c = np.where( presentRoll == rol)
                # if c>0:
                   #presentRoll = np.append(rol)
                # attendance.year = details['lecture_year']
                # attendance.shift = details['lecture_shift']
                # attendance.status = 'Present'
                # attendance.faculty_name = details['faculty_name']
                # attendance.rollnumber = rol
                # attendance.date = details['dt']
                # attendance.lecture_number = details['lecture_no']
                # attendance.save()

                #no = rol[0]

                cv2.putText(img, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))  
            else:
                cv2.putText(img, 'not recognized',
                (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.imshow("Face", img)

        key = cv2.waitKey(10)
        if key == 27:
            break

        attendance.year = details['lecture_year']
        attendance.shift = details['lecture_shift']
        attendance.status = 'Present'
        attendance.faculty_name = details['faculty_name']
        attendance.rollnumber = presentRoll
        attendance.date = details['dt']
        attendance.lecture_number = details['lecture_no']
        attendance.subCode = details['subject']
        attendance.save()
    
    cv2.destroyAllWindows()

    return 1

from pyttsx3 import init
from fd.settings import IMG_ROOT
import numpy as np
import cv2
import os
import keyboard
import pyttsx3

from .models import Attendance, Student

def MarkAttendance(details):    
    attendance = Attendance()
    faceDetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    #datasets = IMG_ROOT + '/'+ +'/'+ 
    datasets = os.path.join(IMG_ROOT,details['lecture_year'],details['lecture_shift'])
    print(datasets)
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
    for (subdir, dir, files) in os.walk(datasets):
        for subdir in files:
            names[id] = subdir
            path = os.path.join(datasets, subdir)
            lable = id
            images.append(cv2.imread(path, 0)) 
            lables.append(int(lable))
        id +=1

    (images, lables) = [np.array(lis) for lis in [images, lables]]
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, lables)  
    cam = cv2.VideoCapture(0)
    sampleNum = 0    
    while keyboard.is_pressed('q')!=True :
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        presentRoll = np.empty(0)
        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (80, 130))
            prediction = model.predict(face_resize)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if prediction[1]<500:  
                stdId=names[prediction[0]]  
                rol = stdId.split('.png')  
                c = np.where( presentRoll == rol)
                if c>0:
                    presentRoll = np.append(rol)
                # attendance.year = details['lecture_year']
                # attendance.shift = details['lecture_shift']
                # attendance.status = 'Present'
                # attendance.faculty_name = details['faculty_name']
                # attendance.rollnumber = presentRoll
                # attendance.date = details['dt']
                # attendance.lecture_number = details['lecture_no']
                # attendance.save()  
                    
                    no = rol[0]

                    try:
                        student = Student.objects.get(rollNumebr = str(no))
                    
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
                        pass
                    
                cv2.putText(img, '% s - %.0f' %(names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))  
            else: 
                cv2.putText(img, 'not recognized',  
                (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
        
        cv2.imshow("Face", img)
        
        key = cv2.waitKey(250)
        if key == 27:
            break
    attendance.year = details['lecture_year']
    attendance.shift = details['lecture_shift']
    attendance.status = 'Present'
    attendance.faculty_name = details['faculty_name']
    attendance.rollnumber = presentRoll
    attendance.date = details['dt']
    attendance.lecture_number = details['lecture_no']
    attendance.save() 
    cv2.destroyAllWindows()
    
    return 1
from fd.settings import IMG_ROOT
import numpy as np
import cv2
import os
import keyboard
import pyttsx3

from .models import Lecture, Attendance, Student

def MarkAttendance(details):    
    attendance = Attendance()
    faceDetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    datasets = IMG_ROOT    
    (images, lables, names, id) = ([], [], {}, 0)
    for (subdir, dir, files) in os.walk(datasets):
        for subdir in dir:
            sub= os.path.join(datasets,subdir)
            for (subdir, dir, files) in os.walk(sub):
                for subdir in dir:
                    subIn = os.path.join(sub,subdir)                    
                    for (subdir, dir, files) in os.walk(subIn):
                        for subdir in files:
                            names[id] = subdir
                            path = os.path.join(subIn, subdir)
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

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (80, 130))
            prediction = model.predict(face_resize)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if prediction[1]<500:  
                stdId=names[prediction[0]]  
                rol = stdId.split('.png')           
                count = Attendance.objects.filter(rollnumber=stdId, lecture_number=details['lecture_no'])
                if not count:
                    attendance.year = details['lecture_year']
                    attendance.shift = details['lecture_shift']
                    attendance.status = 'Present'
                    attendance.faculty_name = details['faculty_name']
                    attendance.rollnumber = rol[0] 
                    attendance.date = details['dt']
                    attendance.lecture_number = details['lecture_no']
                    attendance.save()    

                    student = Student.objects.get(rollNumebr = rol[0])
                    student_name = student.firstname
                    
                    say = student_name + ' attendance marked'

                    speaker = pyttsx3.init()
                    speaker.say(say)
                    speaker.runAndWait()

                cv2.putText(img, '% s - %.0f' %(names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))  
            else: 
                cv2.putText(img, 'not recognized',  
                (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 

        cv2.imshow("Face", img)
        
        key = cv2.waitKey(250)
        if key == 27:
            break
    cv2.destroyAllWindows()
    
    return 1
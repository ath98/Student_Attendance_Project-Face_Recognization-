from django.contrib.messages.api import error
from django.http import request
from django.http import response
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.utils import tree
from django.views.generic import FormView  
import keyboard
import json
import numpy as np
import datetime
from .models import Faculty, Student,Subject,Lecture, Attendance
from .forms import FacultyChoiceField

from .face_detection import saveData

from fd.settings import BASE_DIR, IMG_ROOT

import os
import cv2

# Create your views here.

jsonDec = json.decoder.JSONDecoder()

# method to redirect to login page



@login_required(login_url='login')
def home(request):
    user = request.user.username
    faculty = Faculty.objects.get(username = user)
    assigned_subject = jsonDec.decode(faculty.assigned_subjects)
    assigned_subject_count = 0
    if assigned_subject[0] != "None":
        assigned_subject_count = len(assigned_subject)    
    subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
    lecture_number = Lecture.get_lecture_number()
    print(lecture_number)
    context = {
        'assigned_subject_count' : assigned_subject_count,
        'subjects' : subjects,
        'lecture_number': lecture_number,
    }
    return render(request, 'templates/index.html', context)

# work in progress
@login_required(login_url='login')
def searchFacultyRecord(request):
    if request.method == 'POST':
        username = request.POST['faculty']
        faculty = Faculty.objects.get(username = username)
        assigned_subject = jsonDec.decode(faculty.assigned_subjects)
        subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
        context = {
            'subjects' : subjects,
            'faculty' : faculty,
        }
        return render(request, 'templates/faculty.html', context)
    
    return render('admin')

# method to register faculty
def registerFaculty(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm_password')

        if password == confirmPassword:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'User already exists, try with another username')
                return redirect('login')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'User already exists with email id :' + email + '\ntry with another username')
                return redirect('login')
            else:
                user = User.objects.create_user(
                    username = username,
                    password = password,
                    first_name = firstname,
                    last_name = lastname,
                    email = email
                )
                uf = True

                assigned_subject = ['None']

                faculty = Faculty.objects.create(
                    user = user,
                    firstname = user.first_name,
                    lastname = user.last_name,
                    assigned_subjects = json.dumps(assigned_subject),
                    username = user.username,
                    email = user.email,
                    password = user.password
                )
                faculty.save()
                if uf == True:
                    user.save()
                    
                
                messages.success(request, 'User created succesfully')
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match, Try again')
        
    context = {}
    return render(request, 'templates/login.html')


@login_required(login_url='login')
def admin_page(request):
    faculty_count = Faculty.objects.all().count()
    faculty = Faculty.objects.all()
    sem1_subjects = Subject.objects.filter(semester = 1)
    sem2_subjects = Subject.objects.filter(semester = 2)
    sem3_subjects = Subject.objects.filter(semester = 3)
    sem4_subjects = Subject.objects.filter(semester = 4)
    sem5_subjects = Subject.objects.filter(semester = 5)
    context = {
        'faculty_count' : faculty_count, 
        'faculty': faculty,
        'sem1_subjects': sem1_subjects,
        'sem2_subjects': sem2_subjects,
        'sem3_subjects': sem3_subjects,
        'sem4_subjects': sem4_subjects,
        'sem5_subjects': sem5_subjects,
    }
    return render(request, 'templates/admin.html', context)

def faculty_subject_assign(request):
    if request.method == 'POST':
        faculty_name = request.POST['faculty']
        assigned_subjects = request.POST.getlist('subject[]')
        faculty = Faculty.objects.get(username = faculty_name)
        faculty.assigned_subjects = json.dumps(assigned_subjects)
        faculty.save()

        messages.success(request, 'Subjects assigned to ' + faculty_name + ' successfully.')
        return redirect('admin')
    else:
        return redirect('admin')


# method to display faculty profile
# work in progress
@login_required(login_url='login')
def view_faculty_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        
        faculty = Faculty.objects.filter(username = username)
        context = {
            'faculty':faculty,
        }
        return None




# method to verify user login and do further activities
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        if (username == 'admin') and (password == 'admin'):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password is incorrect')
                return redirect('login')
    else:
        context = {}
        return render(request, 'templates/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def redirect_faculty_profile(request):
    username = request.user.username
    faculty = Faculty.objects.get(username = username)
    assigned_subject = jsonDec.decode(faculty.assigned_subjects)
    subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
    context = {
        'subjects' : subjects,
        'faculty' : faculty,
    }
    return render(request, 'templates/faculty.html', context)

# method to redirect to records page
def redirectViewRecords(request):
    context = {}

# method to update faculty profile
# work in progress
@login_required(login_url='login')
def update_faculty_profile(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # your code goes here:

    context = {}
    return render(request, 'templates/faculty.html', context)


@login_required(login_url='login')
def registerStudent(request):
    
    faceDetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    path = ''
    dataset = IMG_ROOT
    # get values from form fields
    if request.method == 'POST':
        roll = request.POST['rollNumber']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phonenumber = request.POST['phone']
        gender = request.POST['gender']
        shift = request.POST['shift']
        year = request.POST['year']
        
        print("shift:"+shift)
        print("year:"+year)

        s = 0

        if shift == '0':
            s = 1
        elif shift == '1':
            s = 2

        print("shift:"+str(s))

        y = 0

        if year == '51':
            y = 1
        elif year == '52':
            y = 2
        elif year == '53':
            y = 3

        print("year:"+str(y))

        rollNumber = year + shift + roll
        print(rollNumber)
        # assigning those values to the student object
        student = Student()
        student.rollNumebr = rollNumber
        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.phoneNumber = phonenumber
        student.gender = gender
        student.shift = shift
        student.year = year
        
        stat = False
        dataset = IMG_ROOT

        try:
            student = Student.objects.get(rollnumber = rollNumber)
            if student is not None:
                messages.error(request, 'Student with roll number ' + rollNumber + 'already exists.')
                return redirect('registerStudent')
        except:
            stat = False
            paths = os.path.join(dataset, str(y), str(s))
            print("------------------------")
            print(paths)
            print("------------------------")

        # img sample size
        (width, height) = (130, 100)
        cam = cv2.VideoCapture(0)
        sampleNum = 0 
        while(True):
            ret,img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for(x,y,w,h) in faces:
                sampleNum +=1
                img_name = str(rollNumber) + '.png'
                cv2.imwrite(os.path.join(paths, img_name), gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                cv2.waitKey(250)
            cv2.waitKey(1)
            if (sampleNum>2):
                break
        cam.release()
        cv2.destroyAllWindows()
        student.save()
        name = firstname + " " + lastname
        messages.success(request, 'Student ' + name + ' was added successfully')
        return redirect('registerStudent')        
    
    context = {}
    return render(request, 'templates/studentRegistration.html', context)


@login_required(login_url='login')
def createLecture(request):    #get values from the fields lectureid ,subject,profid,profname,shift,year  lecture=take_attendance
    if request.method == 'POST':
        
        faculty_name = request.user.username
        faculty = Faculty.objects.get(username = faculty_name)
        
        lecture = Lecture()
        
        subject = request.POST['subject']
        shift = request.POST['shift']
        year = request.POST['year']
        dt = request.POST['dt']
        tfrom = request.POST['tfrom']
        tto = request.POST['tto']

        date_year = dt.split('-')[0]
        date_month = dt.split('-')[1]
        date_day = dt.split('-')[2]

        lecture_date = datetime.date(int(date_year), int(date_month), int(date_day))
        print(lecture_date)
        
        to_hrs = tto.split(':')[0]
        to_min = tto.split(':')[1]

        lecture_to_time = datetime.time(int(to_hrs), int(to_min))
        print(lecture_to_time)

        from_hrs = tfrom.split(':')[0]
        from_min = tfrom.split(':')[1]

        lecture_from_time = datetime.time(int(from_hrs), int(from_min))
        print(lecture_from_time)

        lecture.subject = subject
        lecture.faculty = faculty
        lecture.shift = shift
        lecture.year = year
        lecture.dt = lecture_date
        lecture.tfrom = lecture_from_time
        lecture.tto = lecture_to_time

        lecture.save()
        return redirect(takeAttendance)
    context = {

    }
    return render(request, 'templates/index.html', context)

@login_required(login_url='login')
def takeAttendance(request):    
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
                lec_id = request.POST.get('lecture_number')
                shift = request.POST.get('shift')
                year = request.POST.get('year')
                dt = request.POST.get('dt')    
                print(shift,year,lec_id)
                count = Attendance.objects.filter(rollnumber=stdId, lecture_number=lec_id)
                if not count:
                    attendance.year = year
                    attendance.shift = shift
                    attendance.status = 'Present'
                    attendance.faculty_name = request.user.username
                    attendance.rollnumber = stdId 
                    attendance.date = dt
                    attendance.lecture_number = lec_id
                    attendance.save()                
            else: 
                cv2.putText(img, 'not recognized',  
                (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 

        cv2.imshow("Face", img)
        
        key = cv2.waitKey(10)
        if key == 27:
            break
    cv2.destroyAllWindows()
    context = {}
    return render(request, 'templates/login.html', context)

def reports(request):  
    context = {}
    return render(request,'templates/reports.html',context)
        
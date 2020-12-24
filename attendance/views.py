from django.contrib.messages.api import error
from django.http import request
from django.http import response
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import tree
from django.views.generic import FormView
import json
import numpy as np
import datetime
import pyttsx3

from .models import Faculty, Student, Subject, Lecture, Attendance
from .forms import CreateStudentForm, CreateFacultyForm
from .reports import *

from .face_detection import MarkAttendance

from fd.settings import BASE_DIR, IMG_ROOT

import os
import cv2

# Create your views here.

jsonDec = json.decoder.JSONDecoder()


@login_required(login_url='login')
def home(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    student_count = Student.objects.count()
    assigned_subject = jsonDec.decode(faculty.assigned_subjects)
    assigned_subject_count = 0
    if assigned_subject[0] != "None":
        assigned_subject_count = len(assigned_subject)
    subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
    lecture_number = Lecture.objects.filter(faculty=faculty).count()
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    context = {
        'assigned_subject_count': assigned_subject_count,
        'subjects': subjects,
        'lecture_number': lecture_number,
        'faculty': faculty,
        'student_count': student_count,
        'profile_url': profile_url,
    }
    return render(request, 'templates/index.html', context)

# work in progress


@login_required(login_url='login')
def searchFacultyRecord(request):
    username = request.user.username
    faculty = Faculty.objects.get(username=username)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    if request.method == 'POST':
        username = request.POST['faculty']
        faculty = Faculty.objects.get(username=username)
        faculty_form = CreateFacultyForm(instance=faculty)
        assigned_subject = jsonDec.decode(faculty.assigned_subjects)
        subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
        context = {
            'subjects': subjects,
            'faculty': faculty,
            'form': faculty_form,
        }
        return render(request, 'templates/faculty.html', context)
    context = {
        'profile_url': profile_url,
    }
    return render('admin')


@login_required(login_url='login')
def faculty_profile(request):
    username = request.user.username
    faculty = Faculty.objects.get(username=username)
    assigned_subject = jsonDec.decode(faculty.assigned_subjects)
    subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
    faculty_form = CreateFacultyForm(instance=faculty)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    context = {
        'subjects': subjects,
        'faculty': faculty,
        'form': faculty_form,
        'profile_url': profile_url,
    }
    return render(request, 'templates/faculty.html', context)


@login_required(login_url='login')
def updateFaculty(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    if request.method == 'POST':
        context = {}
        try:
            faculty = Faculty.objects.get(username=request.POST['username'])
            updateFacultyForm = CreateFacultyForm(
                data=request.POST, files=request.FILES, instance=faculty)
            if updateFacultyForm.is_valid():
                updateFacultyForm.save()
                messages.success(request, 'Profile updated Successfully')
                return redirect('home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('home')

    context = {
        'profile_url': profile_url,
    }
    return render(request, 'templates/faculty.html', context)


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
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, 'User already exists, try with another username')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'User already exists with email id :' +
                               email + '\ntry with another username')
                return redirect('login')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=firstname,
                    last_name=lastname,
                    email=email
                )
                uf = True

                assigned_subject = ['None']

                faculty = Faculty.objects.create(
                    user=user,
                    firstname=user.first_name,
                    lastname=user.last_name,
                    assigned_subjects=json.dumps(assigned_subject),
                    username=user.username,
                    email=user.email,
                    password=user.password
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
    student_count = Student.objects.all().count()
    faculty = Faculty.objects.all()
    lecture_count = Lecture.get_lecture_number()
    sem1_subjects = Subject.objects.filter(semester=1)
    sem2_subjects = Subject.objects.filter(semester=2)
    sem3_subjects = Subject.objects.filter(semester=3)
    sem4_subjects = Subject.objects.filter(semester=4)
    sem5_subjects = Subject.objects.filter(semester=5)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    context = {
        'faculty_count': faculty_count,
        'student_count': student_count,
        'faculty': faculty,
        'sem1_subjects': sem1_subjects,
        'sem2_subjects': sem2_subjects,
        'sem3_subjects': sem3_subjects,
        'sem4_subjects': sem4_subjects,
        'sem5_subjects': sem5_subjects,
        'profile_url': profile_url,
        'lecture_count': lecture_count,
    }
    return render(request, 'templates/admin.html', context)


def faculty_subject_assign(request):
    if request.method == 'POST':
        faculty_name = request.POST['faculty']
        assigned_subjects = request.POST.getlist('subject[]')
        faculty = Faculty.objects.get(username=faculty_name)
        faculty.assigned_subjects = json.dumps(assigned_subjects)
        faculty.save()

        messages.success(request, 'Subjects assigned to ' +
                         faculty_name + ' successfully.')
        return redirect('admin')
    else:
        return redirect('admin')


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

# method to redirect to records page


def redirectViewRecords(request):
    context = {}


@login_required(login_url='login')
def registerStudent(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
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

        s = 0

        if shift == '0':
            s = 1
        elif shift == '1':
            s = 2

        y = 0

        if year == '51':
            y = 1
        elif year == '52':
            y = 2
        elif year == '53':
            y = 3

        rollNumber = year + shift + roll

        # assigning those values to the student object
        student = Student()
        student.rollNumber = rollNumber
        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.phoneNumber = phonenumber
        student.gender = gender
        student.shift = s
        student.year = y

        stat = False
        dataset = IMG_ROOT

        try:
            student = Student.objects.get(rollnumber=rollNumber)
            if student is not None:
                messages.error(request, 'Student with roll number ' +
                               rollNumber + 'already exists.')
                return redirect('registerStudent')
        except:
            stat = False
            paths = os.path.join(dataset, str(y), str(s))
            path = os.path.join(paths, rollNumber)
            os.mkdir(path)

        # img sample size
        (width, height) = (130, 100)
        cam = cv2.VideoCapture(0)
        sampleNum = 0
        say = 'Capturing your face, stay stable'
        speaker = pyttsx3.init()
        voice_rate = 150
        speaker.setProperty('rate', voice_rate)
        speaker.say(say)
        speaker.runAndWait()
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for(x, y, w, h) in faces:
                sampleNum += 1
                img_name = str(sampleNum) + '.png'
                cv2.imwrite(os.path.join(path, img_name), gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.waitKey(250)
            cv2.waitKey(10)
            cv2.imshow("Registration", img)
            if (sampleNum > 14):
                break
        cam.release()
        cv2.destroyAllWindows()
        student.save()
        name = firstname + " " + lastname
        messages.success(request, 'Student ' + name +
                         ' was added successfully')
        return redirect('registerStudent')

    context = {
        'profile_url': profile_url,
    }
    return render(request, 'templates/studentRegistration.html', context)


@login_required(login_url='login')
# get values from the fields lectureid ,subject,profid,profname,shift,year  lecture=take_attendance
def createLecture(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    if request.method == 'POST':

        faculty_name = request.user.username
        faculty = Faculty.objects.get(username=faculty_name)

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

        lecture_date = datetime.date(
            int(date_year), int(date_month), int(date_day))

        to_hrs = tto.split(':')[0]
        to_min = tto.split(':')[1]

        lecture_to_time = datetime.time(int(to_hrs), int(to_min))

        from_hrs = tfrom.split(':')[0]
        from_min = tfrom.split(':')[1]

        lecture_from_time = datetime.time(int(from_hrs), int(from_min))
        lecture.subject = subject
        lecture.faculty = faculty
        lecture.shift = shift
        lecture.year = year
        lecture.dt = lecture_date
        lecture.tfrom = lecture_from_time
        lecture.tto = lecture_to_time

        lecture_no = lecture.lecture_number

        details = {
            'lecture_no': lecture_no,
            'lecture_shift': shift,
            'lecture_year': year,
            'dt': dt,
            'faculty_name': faculty_name,
            'subject': subject,
        }

        success = 0

        datasets = os.path.join(
            IMG_ROOT, details['lecture_year'], details['lecture_shift'])
        if not os.listdir(datasets):
            messages.error(
                request, 'No student record found in dataset, Register student first.')
            return redirect('home')
        else:
            success = MarkAttendance(details)

        if success == 1:
            lecture.save()
            return redirect(home)

    context = {
        'profile_url': profile_url,
    }
    return render(request, 'templates/index.html', context)


@login_required(login_url='login')
def updateStudentRedirect(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    context = {
        'profile_url': profile_url,
    }
    if request.method == 'POST':
        try:
            rollNumber = request.POST['rollNumber']
            shift = request.POST['shift']
            year = request.POST['year']
            student = Student.objects.get(
                rollNumber=rollNumber, shift=shift, year=year)

            updateStudentForm = CreateStudentForm(instance=student)
            context = {
                'form': updateStudentForm,
                'rollNumber': rollNumber,
                'student': student
            }
        except:
            messages.error(request, 'Student Not Found')
            return redirect('admin')
    return render(request, 'templates/student_update.html', context)


@login_required(login_url='login')
def updateStudent(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(
                rollNumber=request.POST['rollNumber'])
            updateStudentForm = CreateStudentForm(
                data=request.POST, instance=student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('admin')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('admin')
    context = {
        'profile_url': profile_url,
    }
    return render(request, 'templates/student_update.html', context)


@login_required(login_url='login')
def reports(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    assigned_subject = jsonDec.decode(faculty.assigned_subjects)
    subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'

    context = {
        'profile_url': profile_url,
        'subjects': subjects,
    }
    return render(request, 'templates/reports.html', context)


@login_required(login_url='login')
def tables(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    assigned_subject = jsonDec.decode(faculty.assigned_subjects)
    subjects = Subject.objects.filter(subject_code__in=(assigned_subject))
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'

    reportType = int(request.POST.get('selectReport'))
    rep = report()
    context = {}
    if reportType == 1:
        lecId = request.POST.get("ID")
        context = rep.byLecture(lecId, request)
        if not bool(context):
            messages.error('Entered Lecture ID is incorrect')
            return redirect(request, 'reports')
        context.update({'profile_url': profile_url})
        return render(request, 'templates/table.html', context)
    if reportType == 3:
        id = request.POST.get('roll')
        code = request.POST.get('sub_code')
        details = {
            'id': id,
            'code': code,
            'profile_url':profile_url,
        }
        context = rep.byDefaulter(details)
        context.update({'profile_url': profile_url})        
        if not bool(context):
            messages.error(request, 'Entered details are incorrect')
            return redirect('reports')
        return render(request, 'templates/rep.html', context)
    if reportType == 2:
        roll = request.POST.get("roll")
        details = {
            'roll': roll,
        }
        context = rep.reportsByRoll(details)
        if not bool(context):
            messages.error(request, 'Entered Roll Number is incorrect')
            return redirect('reports')
        context.update({'profile_url': profile_url})
        return render(request, 'templates/rep2.html', context)


@login_required(login_url='login')
def redirectCalender(request):
    user = request.user.username
    faculty = Faculty.objects.get(username=user)
    try:
        profile_url = faculty.profile_pic.url
    except:
        profile_url = 'None'
    context = {
        'profile_url': profile_url,
    }
    return render(request, 'templates/calender.html', context)

from django.contrib.messages.api import error
from django.http import request
from django.http import response
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView  

from .models import Faculty, Student,Subject
from .forms import FacultyChoiceField

from .face_detection import saveData

from fd.settings import BASE_DIR

import os
import cv2

# Create your views here.

# method to redirect to login page

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'templates/index.html', context)

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
                user.save()

                faculty = Faculty.objects.create(
                    user = user,
                    firstname = user.first_name,
                    lastname = user.last_name,
                    username = user.username,
                    email = user.email,
                    password = user.password
                )
                faculty.save()

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
        assigned_subjects = request.POST.getlist('subject[]')
        print(assigned_subjects)

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
    context = {}
    return render(request, 'templates/faculty.html', context)

# method to redirect to records page
def redirectViewRecords(request):
    context = {}

# method to update faculty profile
@login_required(login_url='login')
def update_faculty_profile(request):
    if request.method == 'POST' and request.FILES['profile_pic']:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        profile_pic = request.FILES['profile_pic']     
         

    context = {}
    return render(request, 'templates/faculty.html', context)


@login_required(login_url='login')
def registerStudent(request):
    # get values from form fields
    if request.method == 'POST':
        rollnumber = request.POST['rollNumber']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phonenumber = request.POST['phone']
        gender = request.POST['gender']
        shift = request.POST['shift']
        year = request.POST['year']

        # assigning those values to the student object
        student = Student()
        student.rollNumebr = rollnumber
        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.phoneNumber = phonenumber
        student.gender = gender
        student.shift = shift
        student.year = year

        stat = False
        try:
            student = Student.objects.get(rollnumber = rollnumber)
            stat = true
        except:
            stat = False

        if (stat == False):
            details = {
                'rollnumber' : rollnumber,
                'shift' : shift,
                'year' : year 
            }

            save_face_data = saveData(details)
            if(save_face_data):
                student.save()
                name = firstname + " " + lastname
                messages.success(request, 'Student ' + name + ' was added successfully')
            else:
                messages.error(request, 'Unable to capture student image')
        else:
            messages.error(request, 'Student with roll number ' + rollnumber + 'already exists.')
            return redirect('home')
        
    context = {}
    return render(request, 'templates/login.html', context)

@login_required(login_url='login')
def takeAttendance(request):
    print(cv2.__version__)
    # Detect face
    # Creating a cascade image classifier
    #faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faceDetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    print(faceDetect)

    dataset = os.path.join(BASE_DIR, 'datasets', 'test')
    print(dataset)
    path = 'G:/project/fd/attendance/0.jpg'
    # im = Image.open("G:/project/fd/attendance/0.jpg")
    # im.show()
    print(BASE_DIR)

    path = BASE_DIR.joinpath('dataset')
    print(path)

    # image = cv2.imread(path)
    # while(True):
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #     faces = faceCascade.detectMultiScale(
    #         gray,
    #         scaleFactor=1.3,
    #         minNeighbors=3,
    #         minSize=(30, 30)
    #     )

    #     for (x, y, w, h) in faces:
    #         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #     cv2.imshow("Face", image)

    # camture images from the webcam and process and detect the face
    # takes video capture id, for webcam most of the time its 0.
    cam = cv2.VideoCapture(0)

    # Our identifier
    # We will put the id here and we will store the id with a face, so that later we can identify whose face it is
    # Our dataset naming counter
    sampleNum = 0
    # Capturing the faces one by one and detect the faces and showing it on the window
    while(True):
        # Capturing the image
        # cam.read will return the status variable and the captured colored image
        ret, img = cam.read()
        # the returned img is a colored image but for the classifier to work we need a greyscale image
        # to convert
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # To store the faces
        # This will detect all the images in the current frame, and it will return the coordinates of the faces
        # Takes in image and some other parameter for accurate result
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        # In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
        for(x, y, w, h) in faces:
            # Whenever the program captures the face, we will write that is a folder
            # Before capturing the face, we need to tell the script whose face it is
            # For that we will need an identifier, here we call it id
            # So now we captured a face, we need to write it in a file
            sampleNum = sampleNum+1
            # Saving the image dataset, but only the face part, cropping the rest
            cv2.imwrite(path + str(sampleNum)+'.jpg', gray[y:y+h, x:x+w])
            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            cv2.waitKey(250)

        # Showing the image in another window
        # Creates a window with window name "Face" and with the image img
        cv2.imshow("Face", img)
        # Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        cv2.waitKey(1)
        # To get out of the loop
        if(sampleNum > 50):
            break
    # releasing the cam
    cam.release()
    # destroying all the windows
    cv2.destroyAllWindows()

    context = {}
    return render(request, 'templates/login.html', context)

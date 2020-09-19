from .models import Student
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .face_detection import saveData

from fd.settings import BASE_DIR



import os
import cv2

# Create your views here.

# method to redirect to login page


def home(request):
    context = {}
    return render(request, 'templates/login.html', context)

# method to verify user login and do further activities


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if (username == 'admin') and (password == 'admin'):
            flag = True

        context = {}
        if flag:
            return render(request, 'templates/index.html', context)
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'templates/login.html', context)

# method to redirect to student registration


def redirectRegisterStudent(request):
    context = {}
    return render(request, 'templates/studentRegistration.html', context)

# method to redirect to records page


def redirectViewRecords(request):
    context = {}

# method to register student


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

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.urls import reverse_lazy
from fda.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
from datetime import date, time
from .models import Image, Student, Attendance
from .forms import CreateStudentForm
from .face_recognition_api.recognizer import captureImage

# Create your views here.


def register_student(request):
    #studentForm = CreateStudentForm()
    if request.method == 'POST':
        #studentForm = CreateStudentForm(data=request.POST, files=request.files)
        stat = False

        rollNumber = request.POST['rollNumber']
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        gender = request.POST['male']
        email = request.POST['email']
        phoneNumber = request.POST['phone']
        year = request.POST['year']
        shift = request.POST['shift']

        details = {
            'rollNumber': rollNumber,
            'year': year,
            'shift': shift
        }

        try:
            student = Student.objects.get(rollNumber)
            stat = True
        except:
            stat = False

        if (stat == False):

            student = Student()

            print('Student form is valid')

            student.rollNumber = rollNumber
            student.firstname = firstname
            student.lastname = lastname
            student.gender = gender
            student.email = email
            student.phoneNumber = phoneNumber
            student.year = year
            student.shift = shift
            student.image = captureImage(details)

            student.save()

            messages.success(request, 'Student ' + firstName +
                             ' ' + lastName + ' was added successfully.')
            return redirect('studentRegistration')
        else:
            messages.error(request, 'Student with Roll Number ' +
                           request.POST['rollNumber'] + ' already exists.')
            return redirect('studentRegistration')
        return render(request, 'registration/index.html')

    return render(request, 'student/index.html')


def register(request):
    if (request.method == 'POST'):
        rollNumber = request.POST['rollNumber']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        year = request.POST['year']
        shift = request.POST['shift']
        gender_male = request.POST['male']
        gender_female = request.POST['female']
        img = request.FILES.get('student_file')
        print(img)
        student = Student()
        print(MEDIA_ROOT)
        print("Roll Number: "+rollNumber)
        print("Student Name : "+firstname+' '+lastname)
        print("Email : "+email)
        print("Phone Number : "+phone)
        print("Year : " + year)
        print("Shift : " + shift)
        f = open(MEDIA_ROOT + '/face_data/'+rollNumber+'.jpg', 'wb')
        f.write(request.raw_post_data)
        f.close()

        student.save()
        print("data recieved")
        return HttpResponse('http://localhost:8080/js/webcamimages/'+rollNumber+'.jpg')
    else:
        print("Error")
        return HttpResponse("Error")

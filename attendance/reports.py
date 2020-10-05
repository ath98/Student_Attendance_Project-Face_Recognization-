from .models import Attendance, Subject, Student
from django.http import request
from django.shortcuts import render

def byLecture(request):  # GET REPORTS OF WHOLE LECTURE
    
    if request.method == 'POST':
        lecId = request.POST.get("ID")
        obj = Attendance.objects.filter(lecture_number=lecId)
        context = {
            'obj': obj
        }
        return render(request, 'templates/reports.html', context)


def byDefaulter(request):  # GET REPORTS OF A SPECIFIC STUDENT AND SUBJECT
    if request.method == 'POST':
        roll = request.POST.get("roll")
        code = request.POST.get("sub_code")
        obj = Attendance.objects.filter(rollnumber=roll, status="Present")
        sub = Subject.objects.get(subject_code=code)
        for i in obj.status:
            if(i == 'Present'):
                count = count + 1
        context = {
            'obj': obj,
            'sub': sub
        }
        return render(request, 'templates/reports.html', context)


def reportsByRoll(request):  # GET REPORTS BY ROLL NUMBER FOR ALL SUBJECTS
    if request.method == 'POST':
        roll = request.POST.get("roll")
        obj = Attendance.objects.get(rollnumber=roll)
        context = {
            'obj': obj
        }
        return render(request, 'templates/reports.html', context)

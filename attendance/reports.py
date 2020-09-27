from .models import Attendance
from django.http import request
from django.shortcuts import render

def byLecture(request): #GET REPORTS OF WHOLE LECTURE
    if request.method == 'POST':
        lecId = request.POST.get("ID")
        obj = Attendance.objects.get(lecture_number= lecId)
        return render(request,'templates/reports.html', obj)      

def byDefaulter(request): #GET REPORTS OF A SPECIFIC STUDENT AND SUBJECT
    if request.method == 'POST':
        roll = request.POST.get("roll")
        shift = request.POST.get("shift")
        obj = Attendance.objects.filter(rollnumber = roll, shift=shift)        
        return render(request,'templates/reports.html', obj)

def reportsByRoll(request): #GET REPORTS BY ROLL NUMBER FOR ALL SUBJECTS
    if request.method == 'POST':
        roll = request.POST.get("roll")
        obj = Attendance.objects.get(rollnumber = roll)
        return render(request,'templates/reports.html', obj)

        

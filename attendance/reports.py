from .models import Attendance
from django.http import request
from django.shortcuts import render

def byLecture(request):
    if request.method == 'POST':
        lecId = request.POST.get("ID")
        obj = Attendance.objects.get(lecture_number= lecId)
        return render(request,'templates/reports.html', obj)      

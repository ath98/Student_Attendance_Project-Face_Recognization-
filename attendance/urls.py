from django.conf.urls import url
from django.urls import path

from attendance.views import *

urlpatterns = [
    path('', home, name='home'),
    path('registerStudent', registerStudent, name='registerStudent'),
    path('login', loginPage, name='login'),
    path('redirectRegisterStudent', redirectRegisterStudent, name = 'redirectRegisterStudent'),
    path('lecture', lecture, name='lecture'),
    #path('redirectTakeAttendance', redirectAttendance, name = 'redirectTakeAttendance'),
    path('redirectViewRecords', redirectViewRecords, name = 'redirectViewRecords'),
    path('takeAttendance', takeAttendance, name = 'takeAttendance'),
]
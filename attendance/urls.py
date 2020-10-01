from django.conf.urls import url
from django.urls import path

from django.views.generic import TemplateView # <--

from attendance import views

urlpatterns = [
    path('home', views.home, name='home'),
    #path('registerStudent/', registerStudent, name='registerStudent'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name = 'logout'),
    path('register', views.registerFaculty, name = 'register'),
    #path('lecture', views.lecture, name= 'lecture'),
    path('take_attendance', views.take_attendance, name= 'take_attendance'),
    path('update_attendance', views.update_attendance, name = 'update_attendance'),
    path('faculty', views.redirect_faculty_profile, name = 'faculty'),
    path('update_profile', views.update_faculty_profile, name = 'update_profile'),
    #path('redirectRegisterStudent/', redirectRegisterStudent, name = 'redirectRegisterStudent'),
    #path('redirectTakeAttendance', redirectAttendance, name = 'redirectTakeAttendance'),
    #path('redirectViewRecords/', redirectViewRecords, name = 'redirectViewRecords'),
    #path('takeAttendance/', takeAttendance, name = 'takeAttendance'),
]










'''

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
'''





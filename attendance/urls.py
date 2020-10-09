from django.conf.urls import url
from django.urls import path

from . import views as views

urlpatterns = [
    path('home', views.home, name='home'),
    path('admin', views.admin_page, name='admin'),
    path('createLecture', views.createLecture, name='createLecture'),
    path('registerStudent', views.registerStudent, name='registerStudent'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerFaculty, name='register'),
    path('faculty', views.redirect_faculty_profile, name='faculty'),
    path('update_profile', views.update_faculty_profile, name='update_profile'),
    path('faculty_subject_assign', views.faculty_subject_assign,
         name='faculty_subject_assign'),
    path('searchFacultyRecord', views.searchFacultyRecord,
         name='searchFacultyRecord'),
    #path('redirectRegisterStudent/', redirectRegisterStudent, name = 'redirectRegisterStudent'),
    #path('redirectTakeAttendance', redirectAttendance, name = 'redirectTakeAttendance'),
    #path('redirectViewRecords/', redirectViewRecords, name = 'redirectViewRecords'),
    path('takeAttendance', views.takeAttendance, name = 'takeAttendance'),
    path('reports',views.reports,name='reports'),
]
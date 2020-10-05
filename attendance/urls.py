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
    path('faculty', views.redirect_faculty_profile, name = 'faculty'),
    path('update_profile', views.update_faculty_profile, name = 'update_profile'),
    #path('redirectRegisterStudent/', redirectRegisterStudent, name = 'redirectRegisterStudent'),
    #path('redirectTakeAttendance', redirectAttendance, name = 'redirectTakeAttendance'),
    #path('redirectViewRecords/', redirectViewRecords, name = 'redirectViewRecords'),
    #path('takeAttendance/', takeAttendance, name = 'takeAttendance'),
    path('reports',views.reports),
]

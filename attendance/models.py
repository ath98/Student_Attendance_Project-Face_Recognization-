from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

from fd.settings import IMG_ROOT

import os

# Create your models here.


def user_dir_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.firstname + instance.lastname
    filename = name + '.' + ext
    dir_path = os.path.join(IMG_ROOT, 'faculty')
    return 'dir_path/{}'.format(filename)

# Class for professor data
class Faculty(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null= True)
    profile_pic = models.ImageField(
        upload_to=user_dir_path, null=True, blank=True)

    def __str__(self):
        return str(self.firstname + " " + self.lastname)

# Class to Define Subjects with their subject code
class Subject(models.Model):
    subject_code = models.CharField(max_length=200, primary_key=True )
    subject_name = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:self.code + " " + self.subject_name

# Class for student data
class Student(models.Model):

    # defining tuples for the choice fields
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )

    SHIFT = (
        ('1', '1'),
        ('2', '2'),
    )

    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )

    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    rollNumebr = models.CharField(max_length=200, primary_key=True)
    email = models.EmailField(max_length=200, null=True)
    phoneNumber = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    shift = models.CharField(max_length=100, null=True, choices=SHIFT)

    def __str__(self):
        return str(self.rollNumebr)

# Class for attendance data
class Attendance(models.Model):

    # defining tuples for the choices fields
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )

    SHIFT = (
        ('1', '1'),
        ('2', '2'),
    )

    STATUS = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    faculty_name = models.CharField(max_length=200, null=True, blank=True)
    lecture = models.CharField(max_length=200, null=True)
    rollnumber = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    year = models.CharField(max_length=200, null=True, choices=YEAR)
    shift = models.CharField(max_length=200, null=True, choices=SHIFT)
    lecture_number = models.CharField(max_length=200, null=True)
    status = models.CharField(
        max_length=200, null=True, default='Absent', choices=STATUS)

    def __str__(self):
        return str(self.rollnumber + " _ " + str(self.date) + " _ " + str(self.time) + " _ " + str(self.lecture_number) + " _ " + str(self.lecture))

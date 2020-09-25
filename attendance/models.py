from django.db import models

from fd.settings import IMG_ROOT

import os

# Create your models here.


def user_dir_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.firstname + instance.lastname
    filename = name + '.' + ext
    dir_path = os.path.join(IMG_ROOT, 'faculty')
    return 'dir_path/{}'.format(filename)


class Faculty(models.Model):

    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )

    id = models.CharField(max_length=200, primary_key=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    phoneNumber = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    profile_pic = models.ImageField(
        upload_to=user_dir_path, null=True, blank=True)

    def __str__(self):
        return str(self.firstname + " " + self.lastname)


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

class lecture(models.Model):

    #defining tuples for the choice fields
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )

    SHIFT = (
        ('1', '1'),
        ('2', '2'),
    )

    lectureid = models.CharField(max_length=200, primary_key=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    pid = models.CharField(max_length=200)
    profname = models.CharField(max_length=200, null=True)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    shift = models.CharField(max_length=100, null=True, choices=SHIFT)
    dt = models.DateField()

    def __str__(self):
        return str(self.lectureid)




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
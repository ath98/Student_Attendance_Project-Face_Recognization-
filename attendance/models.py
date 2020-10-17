from datetime import datetime
from django.contrib.postgres.fields import jsonb
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

from django.contrib.postgres.fields import JSONField
from django.forms.fields import ChoiceField
from fd.settings import IMG_ROOT

from django.utils.timezone import now


import os

# Create your models here.


def user_dir_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.firstname + '_' + instance.lastname
    filename = name + '.' + ext
    return 'datasets/faculty/{}'.format(filename)

# Class for professor data


class Faculty(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    assigned_subjects = models.TextField(blank=True, null=True, default=["None"])
    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(
        upload_to=user_dir_path, null=True, blank=True)

    def __str__(self):
        return str(self.firstname + " " + self.lastname)

# Class to Define Subjects with their subject code


class Subject(models.Model):

    CODE = (
        # Sem 1
        ('310901', '310901'),
        ('310902', '310902'),
        ('310903', '310903'),
        ('310904', '310904'),
        ('310905', '310905'),
        ('310906', '310906'),
        ('310907', '310907'),
        ('310908', '310908'),

        # Sem 2
        ('310909', '310909'),
        ('310910', '310910'),
        ('310911', '310911'),
        ('310912', '310912'),
        ('310913', '310913'),
        ('310914', '310914'),
        ('310915', '310915'),
        ('310916', '310916'),

        # Sem 3
        ('410901', '410901'),
        ('410902', '410902'),
        ('410903', '410903'),
        ('410904', '410904'),
        ('410905', '410905'),
        ('410906', '410906'),
        ('410907', '410907'),
        ('410908', '410908'),

        # Sem 4
        ('410909', '410909'),
        ('410910', '410910'),
        ('410911', '410911'),
        ('410912', '410912'),
        ('410913', '410913'),
        ('410914', '410914'),
        ('410915', '410915'),
        ('410916', '410916'),

        # Sem 5
        ('510901', '510901'),
        ('510902', '510902'),
        ('510903', '510903'),
        ('510904', '510904'),
        ('510905', '510905'),
        ('510906', '510906'),
        ('510907', '510907'),
    )

    NAME = (
        # Sem 1
        ('C and C++ Programming', 'C and C++ Programming'),
        ('Computer Organization', 'Computer Organization'),
        ('Principles of Programming Practices','Principles of Programming Practices'),
        ('Discrete Mathematics', 'Discrete Mathematics'),
        ('Probability & Statistics', 'Probability & Statistics'),
        ('Business Communications', 'Business Communications'),
        ('C & C++ Laboratory', 'C & C++ Laboratory'),
        ('Open Source Tools Laboratory', 'Open Source Tools Laboratory'),

        # Sem 2
        ('Java Programming', 'Java Programming'),
        ('Data Structures using C', 'Data Structures using C'),
        ('Web Technologies', 'Web Technologies'),
        ('System Analysis & Design', 'System Analysis & Design'),
        ('Management Theory & Practices', 'Management Theory & Practices'),
        ('Web Technologies Laboratory', 'Web Technologies Laboratory'),
        ('Java Programming Laboratory', 'Java Programming Laboratory'),
        ('Data Structures Laboratory', 'Data Structures Laboratory'),

        # Sem 3
        ('Advanced Java', 'Advanced Java'),
        ('DBMS', 'DBMS'),
        ('Operating Systems', 'Operating Systems'),
        ('OOAD', 'OOAD'),
        ('Operations Research', 'Operations Research'),
        ('HBASE Lab', 'HBASE Lab'),
        ('Advance Java Lab', 'Advance Java Lab'),
        ('UML Lab – umbrello', 'UML Lab – umbrello'),

        # Sem 4
        ('Advanced Web Technology', 'Advanced Web Technology'),
        ('Banking and FAM', 'Banking and FAM'),
        ('CN & Information Security', 'CN & Information Security'),
        ('Elective I ', 'Elective I '),
        ('Adv DBMS', 'Adv DBMS'),
        ('WT Lab', 'WT Lab'),
        ('Advance DBMS Lab', 'Advance DBMS Lab'),
        ('Network & Security Lab', 'Network & Security Lab'),

        # Sem 5
        ('Recent Technologies in IT', 'Recent Technologies in IT'),
        ('Software Testing and Quality Assurance',
         'Software Testing and Quality Assurance'),
        ('Software Engineering', 'Software Engineering'),
        ('Data warehousing, data mining and BI',
         'Data warehousing, data mining and BI'),
        ('Elective - II', 'Elective - II'),
        ('RTIT Lab', 'RTIT Lab'),
        ('STQA Lab', 'STQA Lab'),
    )

    SEMESTER = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    )

    TYPE = (
        ('Lecture','Lecture'),
        ('Practical','Practical'),
        ('Guest','Guest'),
    )

    YEAR = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
    )

    subject_code = models.CharField(
        max_length=200, primary_key=True, choices=CODE, blank=True)
    subject_name = models.CharField(max_length=200, null=True, choices=NAME)
    semester = models.CharField(max_length=200, choices=SEMESTER, null=True, blank=True)
    year = models.CharField(max_length=200, choices=YEAR, null=True, blank=True)
    type = models.CharField(max_length=200, choices=TYPE, blank=True, null=True)

    def __str__(self):
        return str(self.subject_code +' _ '+ self.subject_name)

    
# def student_dir_path(instance, filename):
#     name, ext = filename.split(".")
#     name = instance.rollNumber
#     filename = name + '.' + ext
#     return 'datasets/{}/{}/{}'.format(instance.year, instance.shift, filename)


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
    rollNumber = models.CharField(max_length=200, primary_key=True)
    email = models.EmailField(max_length=200, null=True)
    phoneNumber = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    shift = models.CharField(max_length=100, null=True, choices=SHIFT)
    # picture = models.ImageField(upload_to = student_dir_path, null = True, blank = True)

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

    faculty_name = models.CharField(max_length=2000, null=True, blank=True)
    rollnumber = models.TextField(max_length=2000, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    year = models.CharField(max_length=200, null=True, choices=YEAR)
    shift = models.CharField(max_length=200, null=True, choices=SHIFT)
    lecture_number = models.CharField(max_length=200, null=True)
    status = models.CharField(
        max_length=200, null=True, default='Absent', choices=STATUS)

    def __str__(self):
        return str(self.rollnumber + " _ " + str(self.date) + " _ " + str(self.time) + " _ " + self.lecture_number)


class Lecture(models.Model):

    def increment_lecture_number():
        last_lecture = Lecture.objects.all().order_by('lecture_number').last()
        if not last_lecture:
            return 1
        return last_lecture.lecture_number + 1

    def get_lecture_number():
        last_lecture = Lecture.objects.all().order_by('lecture_number').last()
        if not last_lecture:
            return 1
        return last_lecture.lecture_number

    lecture_number = models.IntegerField(primary_key=True, default= increment_lecture_number)
    tfrom =  models.TimeField(blank=True, null=True)
    tto = models.TimeField(blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=CASCADE,  null=True)
    year = models.CharField(max_length=200, null=True, blank=True)
    shift = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)

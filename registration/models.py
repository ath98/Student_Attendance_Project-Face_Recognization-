from django.db import models

from django.contrib.auth.models import User
# Create your models here.


def student_directory_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.rollNumber
    filename = name + '.' + ext
    return 'Student_Images/{}/{}/{}/{}'.format(instance.year, instance.shift, filename)


class Student(models.Model):

    genderOption = (('Male', 'm'), ('female', 'f'))
    yearOption = (('1', '1'), ('2', '2'), ('3', '3'))
    shiftOption = (('1', '1'), ('2', '2'))

    rollNumber = models.IntegerField()
    firstname = models.CharField(max_length=200, null=True, blank=True,)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phoneNumber = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(
        max_length=200, null=True, blank=True, choices=genderOption)
    year = models.CharField(
        max_length=200, null=True, blank=True, choices=yearOption)
    shift = models.CharField(
        max_length=200, null=True, blank=True, choices=shiftOption)
    image = models.ImageField(
        upload_to=student_directory_path, null=True, blank=True)

    def __str__(self):
        return str(self.rollNumber)


class Attendance(models.Model):
    faculty_name = models.CharField(max_length=200, null=True, blank=True)
    student_rollnumber = models.CharField(
        max_length=200, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField(auto_now_add=True, null=True)
    year = models.CharField(max_length=200, null=True)
    shift = models.CharField(max_length=200, null=True)
    period = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, default='Absent')

    def __str__(self):
        return str(self.student_rollnumber+"_"+str(self.date)+"_"+str(self.period))


class Faculty(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return str(self.username)


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='face_data/')

    def __str__(self):
        return self.title

# from faker import Faker
# from .models import Attendance
# import random


# def insert():
#     f = Faker()
#     for i in range(10):
#         for j in range(20):
#             year = 2
#             if 1 % 2 == 0:
#                 shift = 1
#             else:
#                 shift = 2
#             if j % 2 == 0:
#                 status = 'Present'
#             else:
#                 status = 'Absent'
#             f_name = f.name()
#             lecture = "BHIDE"
#             rollnumber = j
#             date = '2020-10-20'
#             time = '01:20'
#             lectureNO = 101+i
#         a = Attendance(year=year, shift=shift, faculty_name=f_name,
#             lecture=lecture, rollnumber=rollnumber, date=date, time=time,
#             lecture_number=lectureNO, status=status)
#         a.save()

# t = insert()
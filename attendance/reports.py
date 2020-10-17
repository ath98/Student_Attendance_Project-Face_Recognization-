from .models import Attendance, Subject, Student, Lecture

class report():

    def byLecture(self,lecId):  # GET REPORTS OF WHOLE LECTURE    
        d = dict()
        obj = Attendance.objects.filter(lecture_number=lecId)#Remember to change after  
        lec = Lecture.objects.get(lecture_number=lecId)    
        sub = Subject.objects.filter(subject_code= lec.subject)
        d['obj'] = obj
        d['sub'] = sub
        return d

 
    def byDefaulter(roll,code):  # GET REPORTS OF A SPECIFIC STUDENT AND SUBJECT

        stu = Student.objects.get(rollNumebr=roll)        
        sub = Subject.objects.get(year= stu.year)
        #att = Attendance.objects.filter(rollnumber=roll, status='Present',)
        lecs = Lecture.objects.filter(subject= code).count()   #Total count of lec
        lec = Attendance.objects.filter(rollnumber=roll)
        for l in lec.all:
            c = Attendance.objects.select_related()
            
            
        context = {
            'stu': obj,
            'sub': sub,
        }
        return context


    # def reportsByRoll(roll):  # GET REPORTS BY ROLL NUMBER FOR ALL SUBJECTS        

    #     fy = '31090'
    #     stu = Student.objects.get(rollNumebr=roll)        
    #     sub = Subject.objects.get(year= stu.year)
    #     att = Attendance.objects.get(rollnumber=roll)
    #     lec = Lecture.objects.get.all()
    #     for l in lec.all:
    #         i = 1
    #         if stu.year == '1':
    #             count = Lecture.objects.get(fy + i
    #         if stu.year == '2':
    #         if stu.year == '3':
            
    #     context = {
    #         'stu': obj,
    #         'sub': sub,
    #     }
    #     return context

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

 
    def byDefaulter(self,details):  # GET REPORTS OF A SPECIFIC STUDENT AND SUBJECT

        stu = Student.objects.get(rollNumber=details['id'])
        sub = Subject.objects.filter(subject_code= details['code']) 
        att = list(Attendance.objects.filter(subCode= details['code']))
        lecs = Lecture.objects.filter(subject= details['code']).count()   #Total count of lec 
        count = 0
        for i in range(len(att)):
            try:                
                if str(att[i]).split('53007'):
                    count+=1       
                per = (count/lecs)*100  #Percentage caluclated here   
                roudPer = round(per,2)
            except:
                pass
        
        context = {
            'stu': stu,
            'sub': sub,
            'att':count,
            'per':roudPer,
            'lecs':lecs,
        }
        return context


    # def reportsByRoll(roll):  # GET REPORTS BY ROLL NUMBER FOR ALL SUBJECTS        

    #     fy = '31090'
    #     stu = Student.objects.get(rollNumebr=roll)       
    #         
        #sub = Subject.objects.filter(year= stu.year) 
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

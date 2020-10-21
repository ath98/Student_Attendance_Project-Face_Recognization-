from .models import Attendance, Subject, Student, Lecture
from datetime import date, timedelta

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
        att = list(Attendance.objects.filter(subCode= details['code'],date__range=[details['ds'], details['dt']]))        
        lecs = Lecture.objects.filter(subject= details['code'], date__range=[details['ds'], details['dt']]).count()   #Total count of lec 
        count = 0
        for i in range(len(att)):
            try:                
                if str(att[i]).split(details['id']):
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


    def reportsByRoll(self, details):  # GET REPORTS BY ROLL NUMBER FOR ALL SUBJECTS       
        
        stu = Student.objects.get(rollNumber=details['roll']) 
        sub = (Subject.objects.filter(year= stu.year))
        lecs = []
        count = []
        per = []
        for i in range(len(sub)): 
            c = 0
            code = str(sub[i])
            lec= Lecture.objects.filter(subject= code).count()
            lecs.append(lec)#TOTAL LECTURES
            if lec == 0:
                count.append(0)
                per.append(0)
            else:
                att=list(Attendance.objects.filter(subCode=code)) #Count of lec attened by stu
                for j in range(len(att)):
                    if str(att[j]).split(details['roll']):
                        c += 1  # COUNT OF ATTENDED 
                count.append(c)
                co = int(count[i])
                le = int(lecs[i])
                p = co/le * 100
                per.append(p)
                count.append

        context = {            
            'sub': sub,
            'lecs':lecs,    
            'att':count,
            'per':per,
        }
        return context

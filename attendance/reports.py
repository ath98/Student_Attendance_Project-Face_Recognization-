from .models import Attendance, Subject, Student, Lecture
from datetime import date, timedelta

class report():

    def byLecture(self,lecId):  # GET REPORTS OF WHOLE LECTURE    
        
        lecCheck = Lecture.objects.get(lecture_number = lecId)
        stdCount = Student.objects.filter(year = lecCheck.year, shift = lecCheck.shift).count()
        students = Student.objects.filter(year = lecCheck.year, shift = lecCheck.shift)
        obj = Attendance.objects.filter(lecture_number=lecId) 
        lec = Lecture.objects.get(lecture_number=lecId)    
        roll = []
        a = []
        sub = Subject.objects.filter(subject_code= lec.subject)
        get = Attendance.objects.get(lecture_number=lecId)
        rep = report()
        roll=rep.filtering(get.rollnumber)
        indRoll =rep.joining(roll)
        print(indRoll)

        present = len(indRoll)
        print(present)
        context = {
            "obj":obj,
            "sub":sub,
            "roll":indRoll,
            "id":lecId,
            "total":stdCount,
            "present":present,
            "stud":students,
        }
        return context

    def filtering(self,roll):  #Massaging up the recived data
        l = roll.replace("[","")
        r = l.replace("]","")
        c = r.replace(",","")
        c1 = c.replace("'","")
        c2 = c1.replace(" ","")
        return c2

    def joining(self,str): #joining indivisual str as a single sting
        r = []
        a = 0
        s = ''
        try:
            for i in range(len(str)):
                if(i%5==0 and i!=0):                                
                    r.append(s)
                    a += 1
                    s = ''
                    s = s + str[i]
                else:
                    s = s+str[i]
        finally:
            r.append(s)
        return r
                

    def byDefaulter(self,details):  # GET REPORTS OF A SPECIFIC STUDENT AND SUBJECT
        stu = Student.objects.get(rollNumber=details['id'])
        sub = Subject.objects.filter(subject_code= details['code']) 
        att = list(Attendance.objects.filter(subCode= details['code']))        
        lecs = Lecture.objects.filter(subject= details['code']).count()   #Total count of lec 
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
        subNames= []
        test = []
        size = range(0,1)
        size2 = range(0,3)
        for i in range(len(sub)): 
            c = 0
            code = str(sub[i])
            lec= Lecture.objects.filter(subject= code).count()
            l = Subject.objects.get(subject_code= code)
            subNames.append(l.subject_name)
            lecs.append(lec)#TOTAL LECTURES
            if lec == 0:
                count.append('0')
                per.append('0')
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
        for i in range(len(per)):
            test.append(subNames[i])
            test.append(lecs[i])
            test.append(count[i])
            test.append(per[i])
            strs = subNames[i]+str(lecs[i])+str(count[i])+str(per[i])            
        print(test)

        context = {     
            'test':test,
            'size':size,
            's':size2,
        }
        return context

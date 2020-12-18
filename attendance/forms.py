from django.db.models import fields
from django.forms import ModelForm
from django import forms

from .models import *

class FacultySubject(forms.ModelForm):  
    error_css_class = 'error'

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

    subject_code = forms.ChoiceField(choices=CODE, required=True )
    subject_name = forms.ChoiceField(choices=NAME, required=True )
    shift_1_faculty = forms.ModelChoiceField(queryset=Faculty.objects.all().order_by('username'))
    shift_2_faculty = forms.ModelChoiceField(queryset=Faculty.objects.all().order_by('username'))


class FacultyChoiceField(forms.Form):
    faculty_name = forms.ModelChoiceField(queryset=Faculty.objects.values_list("username", flat=True).distinct(),
        empty_label=None)


class CreateFacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user','assigned_subjects','password']
    def __init__(self, *args, **kwargs):
        super(CreateFacultyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'    

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
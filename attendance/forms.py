from django.forms import ModelForm
from django.forms import widget
from django import forms

from .models import *

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
    firstname = forms.CharField(label = 'firstname', max_length= 200, required=True, widget = forms.TextInput(attrs = {'placeholder' : 'Enter First Name'}))
    lastname = forms.CharField(label = 'lastname', max_length= 200, required=True, widget = forms.TextInput(attrs = {'placeholder' : 'Enter last Name'}))
    email = forms.EmailField(label = 'email', max_length= 200, required=True, widget = forms.EmailField(attrs = {'placeholder' : 'something@example.com'}))
    phonenumber = forms.CharField(lable = '', max_length= 200, required=False, widget = forms.CharField(attrs = {'placeholder' : '1234567890'}))
    gender = forms.ChoiceField(label = 'gender', choices=[Student.GENDER], required=True)
    rollNumber = forms.CharField(label = 'rollnumber', max_length= 200, required=True, widget = forms.TextInput(attrs = {'placeholder' : 'Enter Roll Number'}))
    year = forms.ChoiceField(label = 'year', choices=[Student.YEAR], required=True)
    shift = forms.ChoiceField(label = 'shift', choices=[Student.SHIFT], required=True)

class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'    
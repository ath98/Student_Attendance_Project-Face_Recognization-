from .models import Faculty, Student
from django.forms import ModelForm


class CreateStudentForm(ModelForm):
    """Form definition for Student."""

    class Meta:
        """Meta definition for Studentform."""

        model = Student
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.fields.widget.attrs['class'] = 'form-control'


class CreateFacultyForm(ModelForm):

    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# class Student_Form:
#     """ Student Registration Details Upload Form """

#     rollNumber = forms.CharField(label='rollNumber', max_length=6)
#     firstname = forms.CharField(label='firstname', max_length=50)
#     lastname = forms.CharField(label='lastname', max_length=50)
#     gender = [('Male', 'M'), ('Female', 'F')]
#     gender_selected = forms.ChoiceField(
#         label='gender', widget=forms.RadioSelect(choices=gender))
#     email = forms.EmailField(label='email', max_length=100)
#     phoneNumber = forms.CharField(label='phoneNumber')
#     year = forms.IntegerField(label='year')
#     shift = forms.IntegerField(label='shift')
#     image = forms.ImageField(label='Student Data')

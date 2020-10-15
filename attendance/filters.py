from django.contrib.postgres import fields
import django_filters

from .models import Faculty

class FacultyFilter(django_filters.FilterSet):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user','profile_pic']
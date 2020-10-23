from  django import template
from .models import Post
reg = template.Library()

@reg.inclusion_tag('table.html')
def status(roll,stud):
    

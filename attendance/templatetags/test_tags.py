from django import template

register = template.Library()

@register.simple_tag
def status(roll, curr):
    for x in roll:
        print(x)
        if x != curr:
            pass
        else :        
            return "Present"
    return "Absent"

@register.filter
def index(indexable, i):
    return indexable[i]
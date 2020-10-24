from django import template

register = template.Library()

@register.simple_tag
def status(roll, curr):
    for x in roll:
        if x == curr:
            return "Present"
        else:
            return "Absent"
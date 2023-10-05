from django import template
import os

register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value)




@register.filter
def file_extension(value):
    return value.split('.')[-1].lower()

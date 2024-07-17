from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    return value * arg

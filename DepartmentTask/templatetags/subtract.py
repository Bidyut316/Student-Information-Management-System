from django import template

register = template.Library()

@register.simple_tag
def subtract(val,arg):
    return val-int(arg)

register.filter('subtract', subtract)



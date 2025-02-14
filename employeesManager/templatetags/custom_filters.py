from django import template

register = template.Library()

@register.filter
def get_id(employee):
    return employee.get('_id')
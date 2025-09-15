from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Get value from a dictionary safely"""
    if not d:
        return None
    return d.get(key)

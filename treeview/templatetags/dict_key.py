from django import template


register = template.Library()

@register.filter(name='dict_key')
def dict_key(dict, key):
    """Returns the given key from a dictionary."""
    return dict[key]
__all__ = ()

from django import template

register = template.Library()


@register.filter
def ltruncatechars(value, length):
    if len(value) > length:
        return '...' + value[-length:]

    return value

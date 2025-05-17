__all__ = ()

from django import template

register = template.Library()


@register.simple_tag
def params_replace(request, append=False, **kwargs):
    params = request.GET.copy()
    if append:
        params.update(kwargs)
    else:
        for key, value in kwargs.items():
            if value:
                params[key] = value
            else:
                params.pop(key)

    return params.urlencode()

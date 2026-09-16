from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def split(value, delimiter=","):
    """Split a string by the given delimiter and return a list.

    Usage: {{ value|split:"," }}
    Example: {{ "a,b,c"|split:"," }} -> ["a", "b", "c"]
    """
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]

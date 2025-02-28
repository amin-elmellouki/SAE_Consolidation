import json
from decimal import Decimal

from django import template


register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key)


@register.filter(name='to_json')
def to_json(value):
    if isinstance(value, (list, dict)):
        return json.dumps((value))
    return json.dumps(([value]))

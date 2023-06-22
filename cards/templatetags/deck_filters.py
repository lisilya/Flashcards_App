from django import template
from ..constants import DECK_NAMES

register = template.Library()

@register.filter
def deck_name(deck_number):
    return DECK_NAMES.get(deck_number, 'Unknown')
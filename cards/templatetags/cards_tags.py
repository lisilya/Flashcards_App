from django import template
from cards.models import DECKS, Card

register = template.Library()

@register.inclusion_tag("cards/deck_links.html")
def deck_as_links():
    decks = []
    for deck_num in DECKS:
        card_count = Card.objects.filter(deck=deck_num).count()
        decks.append({
            "number": deck_num,
            "card_count": card_count,
        })

    return {"decks": decks}

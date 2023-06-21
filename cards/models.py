from typing import Any, Dict, Tuple
from django.db import models

# Create your models here.

NUM_DECKS = 5
DECKS = range(1, NUM_DECKS + 1)

class Card(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    deck = models.IntegerField(
        choices=zip(DECKS, DECKS),  # type: ignore
        default=DECKS[0],
        )
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, default="")
    knownAnswerCount = models.IntegerField(default=0)
    unknownAnswerCount = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.question}"
    
    # add .move() method to Card model
    def move(self, solved):
        new_deck = self.deck + 1 if solved else DECKS[0]
        if new_deck in DECKS:
            self.deck = new_deck
            self.save()
        
        return self
    
    # add .delete() method to Card model to delete one card from the DB
    def delete(self, *args, **kwargs):
        super(Card, self).delete(*args, **kwargs)
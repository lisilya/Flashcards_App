from django import forms
from .models import Card
from .constants import DECK_NAMES

class CardCheckForm(forms.Form):
    card_id = forms.IntegerField(required=True)
    solved = forms.BooleanField(required=False)

class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ["question", "answer", "deck", "category"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deck'].choices = [(num, DECK_NAMES.get(num, 'Unknown')) for num, _ in self.fields['deck'].choices]
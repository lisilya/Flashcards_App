from django.shortcuts import render
import random
from collections import defaultdict
from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.shortcuts import get_object_or_404, redirect
from .models import Card
from .forms import CardCheckForm, CardForm
from .constants import DECK_NAMES

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("deck", "-date_created")

class CategoryListView(View):
    def get(self, request):
        cards = Card.objects.all()
        categories = defaultdict(list)
        for card in cards:
            categories[card.category].append(card)
        return render(request, 'cards/category_list.html', {'categories': dict(categories)})

class CardCreateView(CreateView):
    model = Card
    form_class = CardForm
    success_url = reverse_lazy("card-create")

class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")

#add a view for deleting a card by card.id
class CardDeleteView(CardUpdateView, DeleteView):
    def get(self, request, *args, **kwargs):
        card = Card.objects.filter(pk=self.kwargs["pk"]).first()
        if card is not None:
            card.delete()

        if 'edit/' in request.META.get('HTTP_REFERER', ''):
            return redirect(reverse_lazy('card-list'))
        else:
            return redirect(request.META.get("HTTP_REFERER", reverse_lazy('card-list'))) 

#create a view for a single deck
class DeckView(CardListView):
    template_name = "cards/deck.html"
    form_class = CardCheckForm
    
    def get_queryset(self):
        return Card.objects.filter(deck=self.kwargs["deck_num"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck_number"] = self.kwargs["deck_num"]
        context["deck_name"] = self.deck_name(self.kwargs["deck_num"])  # Add deck name to context
        if self.object_list: # type: ignore
            context["check_card"] = random.choice(self.object_list) # type: ignore
        return context

    def deck_name(self, deck_number):
        return DECK_NAMES.get(deck_number, 'Unknown')   

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) # type: ignore
        if form.is_valid():
            card = get_object_or_404(Card, pk=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])

        return redirect(request.META.get("HTTP_REFERER"))

   
    

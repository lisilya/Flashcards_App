# Removed from django.shortcuts import render
import random
from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from django.shortcuts import get_object_or_404, redirect
from .models import Card
from .forms import CardCheckForm

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("deck", "-date_created")

class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "deck", "category"]
    success_url = reverse_lazy("card-create")

class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")

#create a view for a single deck
class DeckView(CardListView):
    template_name = "cards/deck.html"
    form_class = CardCheckForm

    def get_queryset(self):
        return Card.objects.filter(deck=self.kwargs["deck_num"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck_number"] = self.kwargs["deck_num"]
        if self.object_list: # type: ignore
            context["check_card"] = random.choice(self.object_list) # type: ignore
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) # type: ignore
        if form.is_valid():
            card = get_object_or_404(Card, pk=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])

        return redirect(request.META.get("HTTP_REFERER"))

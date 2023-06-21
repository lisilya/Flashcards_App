from django.urls import path
# Removed: from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        "", 
        views.CardListView.as_view(),
        name="card-list"
        ),
    path(
        "new",
        views.CardCreateView.as_view(),
        name="card-create"
        ),
    path(
        "edit/<int:pk>",
        views.CardUpdateView.as_view(),
        name="card-update"
        ),
    #adding a path for a single deck
    path(
        "deck/<int:deck_num>",
        views.DeckView.as_view(),
        name="deck"
        ),
    #adding a path for deleting a card
    path(
        "delete/<int:pk>",
        views.CardDeleteView.as_view(),
        name="card-delete"
        ),
]

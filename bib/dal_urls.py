from django.urls import path
from . import dal_views
from .models import ZotItem, Reference

app_name = "bib"

urlpatterns = [
    path(
        "book-autocomplete/",
        dal_views.ZotItemAC.as_view(model=ZotItem),
        name="book-autocomplete",
    ),
    path(
        "reference-autocomplete/",
        dal_views.ReferenceAC.as_view(model=Reference),
        name="reference-autocomplete",
    ),
]

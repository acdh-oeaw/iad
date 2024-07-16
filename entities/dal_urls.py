from django.urls import path
from . import dal_views
from .models import *

app_name = "vocabs"

urlpatterns = [
    path("altname-autocomplete/",
        dal_views.AlternativeNameAC.as_view(
            model=AlternativeName,
            create_field="name",
        ),
        name="altname-autocomplete",
    ),
    path("place-autocomplete/",
        dal_views.PlaceAC.as_view(
            model=Place,
            create_field="name",
        ),
        name="place-autocomplete",
    ),
    path("place-autocomplete-search/",
        dal_views.PlaceAC.as_view(model=Place),
        name="place-autocomplete-search",
    ),
    path("city-autocomplete/",
        dal_views.CityAC.as_view(
            model=Place,
            create_field="name",
        ),
        name="city-autocomplete",
    ),
    path("person-autocomplete/",
        dal_views.PersonAC.as_view(
            model=Person,
            create_field="name",
        ),
        name="person-autocomplete",
    ),
    path("institution-autocomplete/",
        dal_views.InstitutionAC.as_view(
            model=Institution,
            create_field="written_name",
        ),
        name="institution-autocomplete",
    ),
]

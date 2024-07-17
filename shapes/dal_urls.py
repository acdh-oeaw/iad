from django.urls import path
from . import dal_views
from .models import Municipality

app_name = "shapes"

urlpatterns = [
    path(
        "municipality-autocomplete/",
        dal_views.MunicipalityAC.as_view(
            model=Municipality,
        ),
        name="municipality-autocomplete",
    ),
    path(
        "municipality-autocomplete-search/",
        dal_views.MunicipalitySearchAC.as_view(
            model=Municipality,
        ),
        name="municipality-autocomplete-search",
    ),
    path(
        "countries-ac/",
        dal_views.CountriesAC.as_view(),
        name="countries-ac",
    ),
    path(
        "counties-ac/",
        dal_views.CountiesAC.as_view(),
        name="counties-ac",
    ),
    path(
        "regions-ac/",
        dal_views.RegionsAC.as_view(),
        name="regions-ac",
    ),
]

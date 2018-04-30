from django.conf.urls import url
from . import views
from . import dal_views
from .models import *

app_name = 'vocabs'

urlpatterns = [
    url(
        r'^altname-autocomplete/$', dal_views.AlternativeNameAC.as_view(
            model=AlternativeName, create_field='name',),
        name='altname-autocomplete',
    ),
    url(
        r'^place-autocomplete/$', dal_views.PlaceAC.as_view(
            model=Place, create_field='name',),
        name='place-autocomplete',
    ),
    url(
        r'^place-autocomplete-search/$', dal_views.PlaceAC.as_view(
            model=Place),
        name='place-autocomplete-search',
    ),
    url(
        r'^city-autocomplete/$', dal_views.CityAC.as_view(
            model=Place, create_field='name',),
        name='city-autocomplete',
    ),
    url(
        r'^person-autocomplete/$', dal_views.PersonAC.as_view(
            model=Person, create_field='name',),
        name='person-autocomplete',
    ),
    url(
        r'^institution-autocomplete/$', dal_views.InstitutionAC.as_view(
            model=Institution, create_field='written_name',),
        name='institution-autocomplete',
    ),
]

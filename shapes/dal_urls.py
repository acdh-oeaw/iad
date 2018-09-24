from django.conf.urls import url
from . import views
from . import dal_views
from . models import *

app_name = 'shapes'

urlpatterns = [
    url(
        r'^municipality-autocomplete/$', dal_views.MunicipalityAC.as_view(
            model=Municipality,),
        name='municipality-autocomplete',
    ),
    url(
        r'^municipality-autocomplete-search/$', dal_views.MunicipalitySearchAC.as_view(
            model=Municipality,),
        name='municipality-autocomplete-search',
    ),
    url(
        r'^countries-ac/$', dal_views.CountriesAC.as_view(),
        name='countries-ac',
    ),
]

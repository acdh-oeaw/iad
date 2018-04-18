from django.conf.urls import url
from . import dal_views
from .models import *

app_name = 'archiv'

urlpatterns = [
    url(
        r'^peraltnameiod-autocomplete/$', dal_views.AltNameAC.as_view(
            model=AltName, create_field='label',),
        name='altname-autocomplete',
    ),
    url(
        r'^period-autocomplete/$', dal_views.PeriodAC.as_view(model=Period),
        name='period-autocomplete',
    ),
]

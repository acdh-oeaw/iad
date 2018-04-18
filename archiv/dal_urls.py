from django.conf.urls import url
from . import dal_views
from .models import *

app_name = 'archiv'

urlpatterns = [
    url(
        r'^altname-autocomplete/$', dal_views.AltNameAC.as_view(
            model=AltName, create_field='label',),
        name='altname-autocomplete',
    ),
]

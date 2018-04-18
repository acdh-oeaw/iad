from django.conf.urls import url
from . import dal_views
from .models import *

app_name = 'bib'

urlpatterns = [
    url(
        r'^book-autocomplete/$', dal_views.BookAC.as_view(model=Book),
        name='book-autocomplete',
    ),
]

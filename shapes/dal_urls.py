from django.conf.urls import url
from . import views
from . import dal_views
from . models import *

app_name = 'shapes'

urlpatterns = [
    url(
        r'^cadastralcommunity-autocomplete/$', dal_views.CadastralCommunityAC.as_view(
            model=CadastralCommunity,),
        name='cadastralcommunity-autocomplete',
    ),
]

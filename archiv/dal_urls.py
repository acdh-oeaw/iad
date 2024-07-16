from django.conf.urls import url
from . import dal_views
from .models import *

app_name = "archiv"

urlpatterns = [
    url(
        r"^site-autocomplete/$",
        dal_views.SiteAC.as_view(model=Site),
        name="site-autocomplete",
    ),
    url(
        r"^altname-autocomplete/$",
        dal_views.AltNameAC.as_view(
            model=AltName,
            create_field="label",
        ),
        name="altname-autocomplete",
    ),
    url(
        r"^altname-autocomplete-no-create/$",
        dal_views.AltNameAC.as_view(model=AltName),
        name="altname-autocomplete-no-create",
    ),
    url(
        r"^period-autocomplete/$",
        dal_views.PeriodAC.as_view(model=Period),
        name="period-autocomplete",
    ),
    url(
        r"^researchevent-autocomplete/$",
        dal_views.ResearchEventAC.as_view(model=ResearchEvent),
        name="researchevent-autocomplete",
    ),
    url(
        r"^researchquestion-autocomplete/$",
        dal_views.ResearchQuestionAC.as_view(
            model=ResearchQuestion, create_field="question"
        ),
        name="researchquestion-autocomplete",
    ),
]

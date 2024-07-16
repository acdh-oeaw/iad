from django.urls import path
from . import dal_views
from .models import *

app_name = "archiv"

urlpatterns = [
    path("site-autocomplete/",
        dal_views.SiteAC.as_view(model=Site),
        name="site-autocomplete",
    ),
    path("altname-autocomplete/",
        dal_views.AltNameAC.as_view(
            model=AltName,
            create_field="label",
        ),
        name="altname-autocomplete",
    ),
    path("altname-autocomplete-no-create/",
        dal_views.AltNameAC.as_view(model=AltName),
        name="altname-autocomplete-no-create",
    ),
    path("period-autocomplete/",
        dal_views.PeriodAC.as_view(model=Period),
        name="period-autocomplete",
    ),
    path("researchevent-autocomplete/",
        dal_views.ResearchEventAC.as_view(model=ResearchEvent),
        name="researchevent-autocomplete",
    ),
    path("researchquestion-autocomplete/",
        dal_views.ResearchQuestionAC.as_view(
            model=ResearchQuestion, create_field="question"
        ),
        name="researchquestion-autocomplete",
    ),
]

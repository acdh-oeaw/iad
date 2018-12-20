from django.urls import path
from . import views

app_name = 'checks'

urlpatterns = [
    path('poly-exists/<str:model_name>', views.PolygonExists.as_view(), name='poly_exists'),
    path('poly-fits/archents', views.PolyFitsArchEnts.as_view(), name='poly_fits_archents'),
    path('poly-invalid', views.InValidPoly.as_view(), name='invalid_poly'),
    path('poly-invalid', views.InValidPoly.as_view(), name='invalid_poly'),
    path('research-event-check', views.ResearchEventCheck.as_view(), name='research_event_check'),
]

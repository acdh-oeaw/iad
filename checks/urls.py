from django.urls import path
from . import views

app_name = 'checks'

urlpatterns = [
    path('poly-exists/<str:model_name>', views.PolygonExists.as_view(), name='poly_exists'),
]

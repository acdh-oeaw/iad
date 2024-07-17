from django.urls import path
from . import views

app_name = "shapes"

urlpatterns = [
    path(
        "municipality/",
        views.MunicipalityListView.as_view(),
        name="browse_municipality",
    ),
    path(
        "municipality/detail/<int:pk>",
        views.MunicipalityDetailView.as_view(),
        name="municipality_detail",
    ),
    path(
        "municipality/create/",
        views.MunicipalityCreate.as_view(),
        name="municipality_create",
    ),
    path(
        "municipality/edit/<int:pk>",
        views.MunicipalityUpdate.as_view(),
        name="municipality_edit",
    ),
    path(
        "municipality/delete/<int:pk>",
        views.MunicipalityDelete.as_view(),
        name="municipality_delete",
    ),
]

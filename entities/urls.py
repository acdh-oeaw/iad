from django.urls import path
from . import views

app_name = "entities"

urlpatterns = [
    path(
        "altnames/",
        views.AlternativeNameListView.as_view(),
        name="alternativename_list",
    ),
    path(
        "altnames/detail/<int:pk>",
        views.AlternativeNameDetailView.as_view(),
        name="alternativename_detail",
    ),
    path(
        "altnames/create/",
        views.AlternativeNameCreate.as_view(),
        name="alternativename_create",
    ),
    path(
        "altnames/edit/<int:pk>",
        views.AlternativeNameUpdate.as_view(),
        name="alternativename_edit",
    ),
    path(
        "altnames/delete/<int:pk>",
        views.AlternativeNameDelete.as_view(),
        name="alternativename_delete",
    ),
    path("place/create/", views.create_place, name="place_create"),
    path(
        "place/detail/<int:pk>",
        views.PlaceDetailView.as_view(),
        name="place_detail",
    ),
    path("place/edit/<int:pk>", views.edit_place, name="place_edit"),
    path(
        "place/delete/<int:pk>",
        views.PlaceDelete.as_view(),
        name="place_delete",
    ),
    path(
        "institution/detail/<int:pk>",
        views.InstitutionDetailView.as_view(),
        name="institution_detail",
    ),
    path(
        "institution/delete/<int:pk>",
        views.InstitutionDelete.as_view(),
        name="institution_delete",
    ),
    path(
        "institution/edit/<int:pk>",
        views.InstitutionUpdate.as_view(),
        name="institution_edit",
    ),
    path(
        "institution/create/",
        views.InstitutionCreate.as_view(),
        name="institution_create",
    ),
    path(
        "persons/create/<int:pk>",
        views.PersonDetailView.as_view(),
        name="person_detail",
    ),
    path("person/create/", views.PersonCreate.as_view(), name="person_create"),
    path(
        "person/edit/<int:pk>",
        views.PersonUpdate.as_view(),
        name="person_edit",
    ),
    path(
        "person/delete/<int:pk>",
        views.PersonDelete.as_view(),
        name="person_delete",
    ),
]

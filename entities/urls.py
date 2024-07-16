from django.conf.urls import url
from . import views

app_name = "entities"

urlpatterns = [
    url(
        r"^altnames/$",
        views.AlternativeNameListView.as_view(),
        name="alternativename_list",
    ),
    url(
        r"^altnames/detail/(?P<pk>[0-9]+)$",
        views.AlternativeNameDetailView.as_view(),
        name="alternativename_detail",
    ),
    url(
        r"^altnames/create/$",
        views.AlternativeNameCreate.as_view(),
        name="alternativename_create",
    ),
    url(
        r"^altnames/edit/(?P<pk>[0-9]+)$",
        views.AlternativeNameUpdate.as_view(),
        name="alternativename_edit",
    ),
    url(
        r"^altnames/delete/(?P<pk>[0-9]+)$",
        views.AlternativeNameDelete.as_view(),
        name="alternativename_delete",
    ),
    url(r"^place/create/$", views.create_place, name="place_create"),
    url(
        r"^place/detail/(?P<pk>[0-9]+)$",
        views.PlaceDetailView.as_view(),
        name="place_detail",
    ),
    url(r"^place/edit/(?P<pk>[0-9]+)$", views.edit_place, name="place_edit"),
    url(
        r"^place/delete/(?P<pk>[0-9]+)$",
        views.PlaceDelete.as_view(),
        name="place_delete",
    ),
    url(
        r"^institution/detail/(?P<pk>[0-9]+)$",
        views.InstitutionDetailView.as_view(),
        name="institution_detail",
    ),
    url(
        r"^institution/delete/(?P<pk>[0-9]+)$",
        views.InstitutionDelete.as_view(),
        name="institution_delete",
    ),
    url(
        r"^institution/edit/(?P<pk>[0-9]+)$",
        views.InstitutionUpdate.as_view(),
        name="institution_edit",
    ),
    url(
        r"^institution/create/$",
        views.InstitutionCreate.as_view(),
        name="institution_create",
    ),
    url(
        r"^persons/create/(?P<pk>[0-9]+)$",
        views.PersonDetailView.as_view(),
        name="person_detail",
    ),
    url(r"^person/create/$", views.PersonCreate.as_view(), name="person_create"),
    url(
        r"^person/edit/(?P<pk>[0-9]+)$",
        views.PersonUpdate.as_view(),
        name="person_edit",
    ),
    url(
        r"^person/delete/(?P<pk>[0-9]+)$",
        views.PersonDelete.as_view(),
        name="person_delete",
    ),
]

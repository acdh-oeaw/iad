from django.urls import path
from . import views

app_name = "browsing"

urlpatterns = [
    path(
        "archivaltnames/",
        views.AltNameListView.as_view(),
        name="browse_archivaltnames",
    ),
    path("places/", views.PlaceListView.as_view(), name="browse_places"),
    path("altnames/", views.AlternativeNameListView.as_view(), name="browse_altnames"),
    path("persons/", views.PersonListView.as_view(), name="browse_persons"),
    path(
        "institutions/",
        views.InstitutionListView.as_view(),
        name="browse_institutions",
    ),
    path("periods/", views.PeriodListView.as_view(), name="browse_periods"),
    path(
        "researchevents/",
        views.ResearchEventListView.as_view(),
        name="browse_researchevents",
    ),
    path(
        "download/researchevent/",
        views.ResearchEventDl.as_view(),
        name="dl_researchevent",
    ),
    path(
        "researchquestions/",
        views.ResearchQuestionListView.as_view(),
        name="browse_researchquestions",
    ),
    path("sites/", views.SiteListView.as_view(), name="browse_sites"),
    path("download/site/", views.SiteDl.as_view(), name="dl_sites"),
    path("archents/", views.ArchEntListView.as_view(), name="browse_archents"),
    path("download/archent/", views.ArchEntDl.as_view(), name="dl_archent"),
    path(
        "monumentprotections/",
        views.MonumentProtectionListView.as_view(),
        name="browse_monumentprotections",
    ),
    path(
        "download/monumentprotection/",
        views.MonumentProtectionDl.as_view(),
        name="dl_monumentprotection",
    ),
    path("references/", views.ReferenceListView.as_view(), name="browse_references"),
    path("map/", views.MapView.as_view(), name="map"),
]

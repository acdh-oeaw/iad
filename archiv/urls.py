from django.urls import path
from . import views
from . import copy_views
from . import geojson_views

app_name = "archiv"

urlpatterns = [
    path(
        "monumentprotection/detail/<int:pk>",
        views.MonumentProtectionDetailView.as_view(),
        name="monumentprotection_detail",
    ),
    path(
        "monumentprotection/create/",
        views.MonumentProtectionCreate.as_view(),
        name="monumentprotection_create",
    ),
    path(
        "monumentprotection/edit/<int:pk>",
        views.MonumentProtectionUpdate.as_view(),
        name="monumentprotection_edit",
    ),
    path(
        "monumentprotection/delete/<int:pk>",
        views.MonumentProtectionDelete.as_view(),
        name="monumentprotection_delete",
    ),
    path(
        "archent/detail/<int:pk>",
        views.ArchEntDetailView.as_view(),
        name="archent_detail",
    ),
    path("archent/create/", views.ArchEntCreate.as_view(), name="archent_create"),
    path(
        "archent/edit/<int:pk>",
        views.ArchEntUpdate.as_view(),
        name="archent_edit",
    ),
    path(
        "archent/delete/<int:pk>",
        views.ArchEntDelete.as_view(),
        name="archent_delete",
    ),
    path("site-geojson/", geojson_views.site_geojson, name="site_geojson"),
    path(
        "site/detail/<int:pk>",
        views.SiteDetailView.as_view(),
        name="site_detail",
    ),
    path("site/create/", views.SiteCreate.as_view(), name="site_create"),
    path("site/edit/<int:pk>", views.SiteUpdate.as_view(), name="site_edit"),
    path("site/delete/<int:pk>", views.SiteDelete.as_view(), name="site_delete"),
    path(
        "period/detail/<int:pk>",
        views.PeriodDetailView.as_view(),
        name="period_detail",
    ),
    path("period/create/", views.PeriodCreate.as_view(), name="period_create"),
    path(
        "period/edit/<int:pk>",
        views.PeriodUpdate.as_view(),
        name="period_edit",
    ),
    path(
        "period/delete/<int:pk>",
        views.PeriodDelete.as_view(),
        name="period_delete",
    ),
    path(
        "altname/detail/<int:pk>",
        views.AltNameDetailView.as_view(),
        name="altname_detail",
    ),
    path("altname/create/", views.AltNameCreate.as_view(), name="altname_create"),
    path(
        "altname/edit/<int:pk>",
        views.AltNameUpdate.as_view(),
        name="altname_edit",
    ),
    path(
        "altname/delete/<int:pk>",
        views.AltNameDelete.as_view(),
        name="altname_delete",
    ),
    path(
        "researchevent/detail/<int:pk>",
        views.ResearchEventDetailView.as_view(),
        name="researchevent_detail",
    ),
    path(
        "researchevent/create/",
        views.ResearchEventCreate.as_view(),
        name="researchevent_create",
    ),
    path(
        "researchevent/edit/<int:pk>",
        views.ResearchEventUpdate.as_view(),
        name="researchevent_edit",
    ),
    path(
        "researchevent/delete/<int:pk>",
        views.ResearchEventDelete.as_view(),
        name="researchevent_delete",
    ),
    path(
        "researchquestion/detail/<int:pk>",
        views.ResearchQuestionDetailView.as_view(),
        name="researchquestion_detail",
    ),
    path(
        "researchquestion/create/",
        views.ResearchQuestionCreate.as_view(),
        name="researchquestion_create",
    ),
    path(
        "researchquestion/edit/<int:pk>",
        views.ResearchQuestionUpdate.as_view(),
        name="researchquestion_edit",
    ),
    path(
        "researchquestion/delete/<int:pk>",
        views.ResearchQuestionDelete.as_view(),
        name="researchquestion_delete",
    ),
    path("copy-poly/", copy_views.copy_site_poly_view, name="copy_poly"),
]

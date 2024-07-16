from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import views
from . import copy_views
from . import geojson_views

app_name = "archiv"

urlpatterns = [
    url(
        r"^monumentprotection/detail/(?P<pk>[0-9]+)$",
        views.MonumentProtectionDetailView.as_view(),
        name="monumentprotection_detail",
    ),
    url(
        r"^monumentprotection/create/$",
        views.MonumentProtectionCreate.as_view(),
        name="monumentprotection_create",
    ),
    url(
        r"^monumentprotection/edit/(?P<pk>[0-9]+)$",
        views.MonumentProtectionUpdate.as_view(),
        name="monumentprotection_edit",
    ),
    url(
        r"^monumentprotection/delete/(?P<pk>[0-9]+)$",
        views.MonumentProtectionDelete.as_view(),
        name="monumentprotection_delete",
    ),
    url(
        r"^archent/detail/(?P<pk>[0-9]+)$",
        views.ArchEntDetailView.as_view(),
        name="archent_detail",
    ),
    url(r"^archent/create/$", views.ArchEntCreate.as_view(), name="archent_create"),
    url(
        r"^archent/edit/(?P<pk>[0-9]+)$",
        views.ArchEntUpdate.as_view(),
        name="archent_edit",
    ),
    url(
        r"^archent/delete/(?P<pk>[0-9]+)$",
        views.ArchEntDelete.as_view(),
        name="archent_delete",
    ),
    url(r"^site-geojson/$", geojson_views.site_geojson, name="site_geojson"),
    url(
        r"^site/detail/(?P<pk>[0-9]+)$",
        views.SiteDetailView.as_view(),
        name="site_detail",
    ),
    url(r"^site/create/$", views.SiteCreate.as_view(), name="site_create"),
    url(r"^site/edit/(?P<pk>[0-9]+)$", views.SiteUpdate.as_view(), name="site_edit"),
    url(
        r"^site/delete/(?P<pk>[0-9]+)$", views.SiteDelete.as_view(), name="site_delete"
    ),
    url(
        r"^period/detail/(?P<pk>[0-9]+)$",
        views.PeriodDetailView.as_view(),
        name="period_detail",
    ),
    url(r"^period/create/$", views.PeriodCreate.as_view(), name="period_create"),
    url(
        r"^period/edit/(?P<pk>[0-9]+)$",
        views.PeriodUpdate.as_view(),
        name="period_edit",
    ),
    url(
        r"^period/delete/(?P<pk>[0-9]+)$",
        views.PeriodDelete.as_view(),
        name="period_delete",
    ),
    url(
        r"^altname/detail/(?P<pk>[0-9]+)$",
        views.AltNameDetailView.as_view(),
        name="altname_detail",
    ),
    url(r"^altname/create/$", views.AltNameCreate.as_view(), name="altname_create"),
    url(
        r"^altname/edit/(?P<pk>[0-9]+)$",
        views.AltNameUpdate.as_view(),
        name="altname_edit",
    ),
    url(
        r"^altname/delete/(?P<pk>[0-9]+)$",
        views.AltNameDelete.as_view(),
        name="altname_delete",
    ),
    url(
        r"^researchevent/detail/(?P<pk>[0-9]+)$",
        views.ResearchEventDetailView.as_view(),
        name="researchevent_detail",
    ),
    url(
        r"^researchevent/create/$",
        views.ResearchEventCreate.as_view(),
        name="researchevent_create",
    ),
    url(
        r"^researchevent/edit/(?P<pk>[0-9]+)$",
        views.ResearchEventUpdate.as_view(),
        name="researchevent_edit",
    ),
    url(
        r"^researchevent/delete/(?P<pk>[0-9]+)$",
        views.ResearchEventDelete.as_view(),
        name="researchevent_delete",
    ),
    url(
        r"^researchquestion/detail/(?P<pk>[0-9]+)$",
        views.ResearchQuestionDetailView.as_view(),
        name="researchquestion_detail",
    ),
    url(
        r"^researchquestion/create/$",
        views.ResearchQuestionCreate.as_view(),
        name="researchquestion_create",
    ),
    url(
        r"^researchquestion/edit/(?P<pk>[0-9]+)$",
        views.ResearchQuestionUpdate.as_view(),
        name="researchquestion_edit",
    ),
    url(
        r"^researchquestion/delete/(?P<pk>[0-9]+)$",
        views.ResearchQuestionDelete.as_view(),
        name="researchquestion_delete",
    ),
    url(r"^copy-poly/$", copy_views.copy_site_poly_view, name="copy_poly"),
]

from django.conf.urls import url
from . import views

app_name = 'archiv'

urlpatterns = [
    url(r'^site/detail/(?P<pk>[0-9]+)$', views.SiteDetailView.as_view(),
        name='site_detail'),
    url(r'^site/create/$', views.SiteCreate.as_view(),
        name='site_create'),
    url(r'^site/edit/(?P<pk>[0-9]+)$', views.SiteUpdate.as_view(),
        name='site_edit'),
    url(r'^site/delete/(?P<pk>[0-9]+)$', views.SiteDelete.as_view(),
        name='site_delete'),
    url(r'^period/detail/(?P<pk>[0-9]+)$', views.PeriodDetailView.as_view(),
        name='period_detail'),
    url(r'^period/create/$', views.PeriodCreate.as_view(),
        name='period_create'),
    url(r'^period/edit/(?P<pk>[0-9]+)$', views.PeriodUpdate.as_view(),
        name='period_edit'),
    url(r'^period/delete/(?P<pk>[0-9]+)$', views.PeriodDelete.as_view(),
        name='period_delete'),
    url(r'^altname/detail/(?P<pk>[0-9]+)$', views.AltNameDetailView.as_view(),
        name='altname_detail'),
    url(r'^altname/create/$', views.AltNameCreate.as_view(),
        name='altname_create'),
    url(r'^altname/edit/(?P<pk>[0-9]+)$', views.AltNameUpdate.as_view(),
        name='altname_edit'),
    url(r'^altname/delete/(?P<pk>[0-9]+)$', views.AltNameDelete.as_view(),
        name='altname_delete'),
    url(r'^researchevent/detail/(?P<pk>[0-9]+)$', views.ResearchEventDetailView.as_view(),
        name='researchevent_detail'),
    url(r'^researchevent/create/$', views.ResearchEventCreate.as_view(),
        name='researchevent_create'),
    url(r'^researchevent/edit/(?P<pk>[0-9]+)$', views.ResearchEventUpdate.as_view(),
        name='researchevent_edit'),
    url(r'^researchevent/delete/(?P<pk>[0-9]+)$', views.ResearchEventDelete.as_view(),
        name='researchevent_delete'),
]

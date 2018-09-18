from django.conf.urls import url
from . import views
from archiv import views as archiv_views

app_name = 'public'

urlpatterns = [
    url(r'sites/$', views.PublicSiteListView.as_view(), name='browse_sites_public'),
    url(
        r'^site/detail/(?P<pk>[0-9]+)$', archiv_views.SiteDetailView.as_view(),
        name='site_detail_public'
    ),
]

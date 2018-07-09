from django.conf.urls import url
from . import views

app_name = 'shapes'

urlpatterns = [
    url(
        r'^municipality/$', views.MunicipalityListView.as_view(),
        name='browse_municipality'
    ),
    url(r'^municipality/detail/(?P<pk>[0-9]+)$', views.MunicipalityDetailView.as_view(),
        name='municipality_detail'),
    url(r'^municipality/create/$', views.MunicipalityCreate.as_view(),
        name='municipality_create'),
    url(r'^municipality/edit/(?P<pk>[0-9]+)$', views.MunicipalityUpdate.as_view(),
        name='municipality_edit'),
    url(r'^municipality/delete/(?P<pk>[0-9]+)$', views.MunicipalityDelete.as_view(),
        name='municipality_delete'),
]

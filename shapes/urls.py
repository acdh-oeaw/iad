from django.conf.urls import url
from . import views

app_name = 'shapes'

urlpatterns = [
    url(
        r'^cadastralcommunity/$', views.CadastralCommunityListView.as_view(),
        name='browse_cadastralcommunity'
    ),
    url(r'^cadastralcommunity/detail/(?P<pk>[0-9]+)$', views.CadastralCommunityDetailView.as_view(),
        name='cadastralcommunity_detail'),
    url(r'^cadastralcommunity/create/$', views.CadastralCommunityCreate.as_view(),
        name='cadastralcommunity_create'),
    url(r'^cadastralcommunity/edit/(?P<pk>[0-9]+)$', views.CadastralCommunityUpdate.as_view(),
        name='cadastralcommunity_edit'),
    url(r'^cadastralcommunity/delete/(?P<pk>[0-9]+)$', views.CadastralCommunityDelete.as_view(),
        name='cadastralcommunity_delete'),
]

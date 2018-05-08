from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from entities.apis_views import PlaceViewSet, GeoJsonViewSet
from bib.api_views import BookViewSet

from vocabs import api_views
from archiv import api_views as archiv_api_views

router = routers.DefaultRouter()
router.register(r'geojson', GeoJsonViewSet, base_name='places')
router.register(r'skoslabels', api_views.SkosLabelViewSet)
router.register(r'skosnamespaces', api_views.SkosNamespaceViewSet)
router.register(r'skosconceptschemes', api_views.SkosConceptSchemeViewSet)
router.register(r'skosconcepts', api_views.SkosConceptViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'Book', BookViewSet)
router.register(r'sites', archiv_api_views.PlaceViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^arche/', include('arche.urls', namespace='arche')),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^sparql/', include('sparql.urls', namespace='sparql')),
    url(r'^vocabs/', include('vocabs.urls', namespace='vocabs')),
    url(r'^vocabs-ac/', include('vocabs.dal_urls', namespace='vocabs-ac')),
    url(r'^archiv-ac/', include('archiv.dal_urls', namespace='archiv-ac')),
    url(r'^entities-ac/', include('entities.dal_urls', namespace='entities-ac')),
    url(r'^entities/', include('entities.urls', namespace='entities')),
    url(r'^bib/', include('bib.urls', namespace='bib')),
    url(r'^bib-ac/', include('bib.dal_urls', namespace='bib-ac')),
    url(r'^archiv/', include('archiv.urls', namespace='archiv')),
    url(r'^', include('webpage.urls', namespace='webpage')),
]

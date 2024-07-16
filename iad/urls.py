from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from bib.api_views import ZotItemViewSet

from vocabs import api_views
from archiv import api_views as archiv_api_views
from shapes import api_views as shapes_api_vies

router = routers.DefaultRouter()
router.register(r"skoslabels", api_views.SkosLabelViewSet)
router.register(r"skosnamespaces", api_views.SkosNamespaceViewSet)
router.register(r"skosconceptschemes", api_views.SkosConceptSchemeViewSet)
router.register(r"skosconcepts", api_views.SkosConceptViewSet)
router.register(r"ZotItem", ZotItemViewSet)
router.register(r"sites", archiv_api_views.SiteViewSet)
# router.register(r'archents', archiv_api_views.ArchEntViewSet)
router.register(r"municipalities", shapes_api_vies.MunicipalityViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("arche/", include("arche.urls", namespace="arche")),
    path("browsing/", include("browsing.urls", namespace="browsing")),
    # path('sparql/', include('sparql.urls', namespace='sparql')),
    path("vocabs/", include("vocabs.urls", namespace="vocabs")),
    path("vocabs-ac/", include("vocabs.dal_urls", namespace="vocabs-ac")),
    path("archiv-ac/", include("archiv.dal_urls", namespace="archiv-ac")),
    path("entities-ac/", include("entities.dal_urls", namespace="entities-ac")),
    path("entities/", include("entities.urls", namespace="entities")),
    path("shapes/", include("shapes.urls", namespace="shapes")),
    path("shapes-ac/", include("shapes.dal_urls", namespace="shapes-ac")),
    path("bib/", include("bib.urls", namespace="bib")),
    path("bib-ac/", include("bib.dal_urls", namespace="bib-ac")),
    path("archiv/", include("archiv.urls", namespace="archiv")),
    path("charts/", include("charts.urls", namespace="charts")),
    path("checks/", include("checks.urls", namespace="checks")),
    path("", include("webpage.urls", namespace="webpage")),
]

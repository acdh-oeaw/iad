from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from browsing.filters import ArchEntListFilter

from .api_serializers import ArchEntSerializer, SiteSerializer
from .models import ArchEnt, Site


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class ArchEntViewSet(viewsets.ModelViewSet):
    queryset = ArchEnt.objects.all()
    serializer_class = ArchEntSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArchEntListFilter

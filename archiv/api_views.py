from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Site, ArchEnt
from .api_serializers import SiteSerializer, ArchEntSerializer
from browsing.filters import ArchEntListFilter


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class ArchEntViewSet(viewsets.ModelViewSet):
    queryset = ArchEnt.objects.all()
    serializer_class = ArchEntSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArchEntListFilter

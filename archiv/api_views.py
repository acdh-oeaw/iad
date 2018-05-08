from rest_framework import viewsets
from .models import Site
from .api_serializers import SiteSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .api_renderers import GeoJsonRenderer
from .models import AlternativeName, Place
from .serializers import AlternativeNameSerializer, GeoJsonSerializer, PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    depth = 2


class AlternativNameViewSet(viewsets.ModelViewSet):
    queryset = AlternativeName.objects.all()
    serializer_class = AlternativeNameSerializer


class GeoJsonViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Place.objects.all()
        serializer = GeoJsonSerializer(queryset, many=True)
        return Response(serializer.data)

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (GeoJsonRenderer,)

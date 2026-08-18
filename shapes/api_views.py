from rest_framework import viewsets

from .api_serializers import MunicipalitySerializer
from .models import Municipality


class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer

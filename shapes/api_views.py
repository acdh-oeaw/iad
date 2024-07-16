from rest_framework import viewsets
from .models import Municipality
from .api_serializers import MunicipalitySerializer


class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer

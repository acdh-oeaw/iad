from rest_framework import viewsets

from bib.models import ZotItem
from bib.serializers import ZotItemSerializer


class ZotItemViewSet(viewsets.ModelViewSet):
    queryset = ZotItem.objects.all()
    serializer_class = ZotItemSerializer

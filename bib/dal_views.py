from dal import autocomplete
from django.db.models import Q
from .models import *


class ZotItemAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ZotItem.objects.all()

        if self.q:
            qs = qs.filter(
                Q(zot_title__icontains=self.q) |
                Q(zot_creator__icontains=self.q) |
                Q(zot_pub_title__icontains=self.q) |
                Q(zot_date__icontains=self.q)
            )

        return qs


class ReferenceAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Reference.objects.all()

        if self.q:
            qs = qs.filter(
                Q(zotero_item__zot_title__icontains=self.q) |
                Q(zotero_item__zot_creator__icontains=self.q)
            )

        return qs

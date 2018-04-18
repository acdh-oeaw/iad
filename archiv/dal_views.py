from dal import autocomplete
from .models import *


class PeriodAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Period.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class AltNameAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AltName.objects.all()

        if self.q:
            qs = qs.filter(label__icontains=self.q)

        return qs

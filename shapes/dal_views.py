from dal import autocomplete
from .models import Municipality
from django.db.models import Q


class MunicipalityAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Municipality.objects.all()

        if self.q:
            qs = qs.filter(
                Q(saunam__icontains=self.q) |
                Q(lau2nam__icontains=self.q) |
                Q(nuts3nam__icontains=self.q)
            )

        return qs

from dal import autocomplete
from .models import Municipality
from django.db.models import Q


class MunicipalityAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Municipality.objects.all()

        if self.q:
            qs = qs.filter(
                Q(lau2nam__icontains=self.q) |
                Q(nuts3nam__icontains=self.q)
            )

        return qs


class MunicipalitySearchAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Municipality.objects.exclude(has_sites=None)

        if self.q:
            qs = qs.filter(
                Q(lau2nam__icontains=self.q) |
                Q(nuts3nam__icontains=self.q)
            )

        return qs


class CountriesAC(autocomplete.Select2ListView):
    def get_list(self):
        values = set(Municipality.objects.values_list('ctnam').distinct())
        countries = [x[0] for x in values]
        return countries

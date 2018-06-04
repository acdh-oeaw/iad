from dal import autocomplete
from .models import CadastralCommunity
from django.db.models import Q


class CadastralCommunityAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CadastralCommunity.objects.all()

        if self.q:
            qs = qs.filter(cadcom_nam__icontains=self.q)

        return qs

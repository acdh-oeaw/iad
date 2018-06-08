from django.db.models import Q
from dal import autocomplete
from .models import *


class ResearchQuestionAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ResearchQuestion.objects.all()

        if self.q:
            qs = qs.filter(question__icontains=self.q)

        return qs


class ResearchEventAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ResearchEvent.objects.all()

        if self.q:
            qs = qs.filter(
                Q(id__icontains=self.q) |
                Q(name__icontains=self.q) |
                Q(research_type__pref_label__icontains=self.q) |
                Q(research_method__pref_label__icontains=self.q) |
                Q(research_question__question__icontains=self.q) |
                Q(responsible_institution__written_name__icontains=self.q)
            )
        return qs


class SiteAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Site.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


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

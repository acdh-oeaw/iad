from django.shortcuts import render

from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import *
from .models import *


class CemeteryDetailView(DetailView):
    model = Cemetery
    template_name = 'archiv/cemetery_detail.html'


class CemeteryCreate(CreateView):

    model = Cemetery
    form_class = CemeteryForm
    template_name = 'archiv/cemetery_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CemeteryCreate, self).dispatch(*args, **kwargs)


class CemeteryUpdate(UpdateView):

    model = Cemetery
    form_class = CemeteryForm
    template_name = 'archiv/cemetery_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CemeteryUpdate, self).dispatch(*args, **kwargs)


class CemeteryDelete(DeleteView):
    model = Cemetery
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_cemeteries')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CemeteryDelete, self).dispatch(*args, **kwargs)


class SettlementDetailView(DetailView):
    model = Settlement
    template_name = 'archiv/settlement_detail.html'


class SettlementCreate(CreateView):

    model = Settlement
    form_class = SettlementForm
    template_name = 'archiv/settlement_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SettlementCreate, self).dispatch(*args, **kwargs)


class SettlementUpdate(UpdateView):

    model = Settlement
    form_class = SettlementForm
    template_name = 'archiv/settlement_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SettlementUpdate, self).dispatch(*args, **kwargs)


class SettlementDelete(DeleteView):
    model = Settlement
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_settlements')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SettlementDelete, self).dispatch(*args, **kwargs)


class SiteDetailView(DetailView):
    model = Site
    template_name = 'archiv/site_detail.html'


class SiteCreate(CreateView):

    model = Site
    form_class = SiteForm
    template_name = 'archiv/site_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SiteCreate, self).dispatch(*args, **kwargs)


class SiteUpdate(UpdateView):

    model = Site
    form_class = SiteForm
    template_name = 'archiv/site_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SiteUpdate, self).dispatch(*args, **kwargs)


class SiteDelete(DeleteView):
    model = Site
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_period')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SiteDelete, self).dispatch(*args, **kwargs)


class ResearchEventDetailView(DetailView):
    model = ResearchEvent
    template_name = 'archiv/researchevent_detail.html'


class ResearchEventCreate(CreateView):

    model = ResearchEvent
    form_class = ResearchEventForm
    template_name = 'archiv/researchevent_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchEventCreate, self).dispatch(*args, **kwargs)


class ResearchEventUpdate(UpdateView):

    model = ResearchEvent
    form_class = ResearchEventForm
    template_name = 'archiv/researchevent_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchEventUpdate, self).dispatch(*args, **kwargs)


class ResearchEventDelete(DeleteView):
    model = ResearchEvent
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_period')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchEventDelete, self).dispatch(*args, **kwargs)


class AltNameDetailView(DetailView):
    model = AltName
    template_name = 'archiv/altname_detail.html'


class AltNameCreate(CreateView):

    model = AltName
    form_class = AltNameForm
    template_name = 'archiv/altname_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AltNameCreate, self).dispatch(*args, **kwargs)


class AltNameUpdate(UpdateView):

    model = AltName
    form_class = AltNameForm
    template_name = 'archiv/altname_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AltNameUpdate, self).dispatch(*args, **kwargs)


class AltNameDelete(DeleteView):
    model = AltName
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_period')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AltNameDelete, self).dispatch(*args, **kwargs)


class PeriodDetailView(DetailView):
    model = Period
    template_name = 'archiv/period_detail.html'


class PeriodCreate(CreateView):

    model = Period
    form_class = PeriodForm
    template_name = 'archiv/period_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeriodCreate, self).dispatch(*args, **kwargs)


class PeriodUpdate(UpdateView):

    model = Period
    form_class = PeriodForm
    template_name = 'archiv/period_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeriodUpdate, self).dispatch(*args, **kwargs)


class PeriodDelete(DeleteView):
    model = Period
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_period')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeriodDelete, self).dispatch(*args, **kwargs)

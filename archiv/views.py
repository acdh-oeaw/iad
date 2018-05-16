from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from reversion.models import Version

from .forms import *
from .models import *


class BaseCreateView(CreateView):
    model = None
    form_class = None
    template_name = 'archiv/generic_create.html'

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data()
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model._meta.verbose_name:
            context['class_name'] = "{}".format(self.model._meta.verbose_name.title())
        else:
            context['class_name'] = "{}".format(self.model.__name__)
        return context


class BaseUpdateView(UpdateView):
    model = None
    form_class = None
    template_name = 'archiv/generic_create.html'

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data()
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model._meta.verbose_name:
            context['class_name'] = "{}".format(self.model._meta.verbose_name.title())
        else:
            context['class_name'] = "{}".format(self.model.__name__)
        return context


class ArchEntDetailView(DetailView):
    model = ArchEnt
    template_name = 'archiv/archent_detail.html'


class ArchEntCreate(BaseCreateView):

    model = ArchEnt
    form_class = ArchEntForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArchEntCreate, self).dispatch(*args, **kwargs)


class ArchEntUpdate(BaseUpdateView):

    model = ArchEnt
    form_class = ArchEntForm

    def get_context_data(self, **kwargs):
        context = super(ArchEntUpdate, self).get_context_data()
        try:
            instance = self.object
            site_poly = instance.site_id.get_geojson()
            context['site_poly'] = "{}".format(site_poly)
        except:
            context['site_poly'] = None
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArchEntUpdate, self).dispatch(*args, **kwargs)


class ArchEntDelete(DeleteView):
    model = ArchEnt
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_archents')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArchEntDelete, self).dispatch(*args, **kwargs)


class SiteDetailView(DetailView):
    model = Site
    template_name = 'archiv/site_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data()
        try:
            information_source = self.object.has_research_activity.order_by('start_date')[0]
        except IndexError:
            information_source = None
        context['information_source'] = information_source
        context['history'] = Version.objects.get_for_object(self.object)
        return context


class SiteCreate(BaseCreateView):

    model = Site
    form_class = SiteForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SiteCreate, self).dispatch(*args, **kwargs)


class SiteUpdate(BaseUpdateView):

    model = Site
    form_class = SiteForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SiteUpdate, self).dispatch(*args, **kwargs)


class SiteDelete(DeleteView):
    model = Site
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_sites')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SiteDelete, self).dispatch(*args, **kwargs)


class ResearchEventDetailView(DetailView):
    model = ResearchEvent
    template_name = 'archiv/researchevent_detail.html'


class ResearchEventCreate(BaseCreateView):

    model = ResearchEvent
    form_class = ResearchEventForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchEventCreate, self).dispatch(*args, **kwargs)


class ResearchEventUpdate(BaseUpdateView):

    model = ResearchEvent
    form_class = ResearchEventForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchEventUpdate, self).dispatch(*args, **kwargs)


class ResearchEventDelete(DeleteView):
    model = ResearchEvent
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_researchevents')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchEventDelete, self).dispatch(*args, **kwargs)


class AltNameDetailView(DetailView):
    model = AltName
    template_name = 'archiv/altname_detail.html'


class AltNameCreate(BaseCreateView):

    model = AltName
    form_class = AltNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AltNameCreate, self).dispatch(*args, **kwargs)


class AltNameUpdate(BaseUpdateView):

    model = AltName
    form_class = AltNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AltNameUpdate, self).dispatch(*args, **kwargs)


class AltNameDelete(DeleteView):
    model = AltName
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_altnames')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AltNameDelete, self).dispatch(*args, **kwargs)


class PeriodDetailView(DetailView):
    model = Period
    template_name = 'archiv/period_detail.html'


class PeriodCreate(BaseCreateView):

    model = Period
    form_class = PeriodForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeriodCreate, self).dispatch(*args, **kwargs)


class PeriodUpdate(BaseUpdateView):

    model = Period
    form_class = PeriodForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeriodUpdate, self).dispatch(*args, **kwargs)


class PeriodDelete(DeleteView):
    model = Period
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_periods')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PeriodDelete, self).dispatch(*args, **kwargs)


class ResearchQuestionDetailView(DetailView):
    model = ResearchQuestion
    template_name = 'archiv/researchquestion_detail.html'


class ResearchQuestionCreate(BaseCreateView):

    model = ResearchQuestion
    form_class = ResearchQuestionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchQuestionCreate, self).dispatch(*args, **kwargs)


class ResearchQuestionUpdate(BaseUpdateView):

    model = ResearchQuestion
    form_class = ResearchQuestionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchQuestionUpdate, self).dispatch(*args, **kwargs)


class ResearchQuestionDelete(DeleteView):
    model = ResearchQuestion
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_researchquestions')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResearchQuestionDelete, self).dispatch(*args, **kwargs)


class MonumentProtectionDetailView(DetailView):
    model = MonumentProtection
    template_name = 'archiv/monumentprotection_detail.html'


class MonumentProtectionCreate(BaseCreateView):

    model = MonumentProtection
    form_class = MonumentProtectionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MonumentProtectionCreate, self).dispatch(*args, **kwargs)


class MonumentProtectionUpdate(BaseUpdateView):

    model = MonumentProtection
    form_class = MonumentProtectionForm

    def get_context_data(self, **kwargs):
        context = super(MonumentProtectionUpdate, self).get_context_data()
        try:
            instance = self.object
            site_poly = instance.site_id.get_geojson()
            context['site_poly'] = "{}".format(site_poly)
        except:
            context['site_poly'] = None
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MonumentProtectionUpdate, self).dispatch(*args, **kwargs)


class MonumentProtectionDelete(DeleteView):
    model = MonumentProtection
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_monumentprotections')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MonumentProtectionDelete, self).dispatch(*args, **kwargs)

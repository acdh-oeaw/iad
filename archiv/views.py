from django.shortcuts import render

from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PeriodForm, AltNameForm
from .models import Period, AltName


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

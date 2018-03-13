from django.shortcuts import render

from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PeriodForm
from .models import Period


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

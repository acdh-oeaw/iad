from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_tables2 import RequestConfig

from .models import Municipality
from .tables import MunicipalityTable
from .filters import MunicipalityListFilter
from .forms import MunicipalityFilterFormHelper, MunicipalityForm

from webpage.utils import GenericListView, BaseCreateView, BaseUpdateView


class MunicipalityListView(GenericListView):
    model = Municipality
    table_class = MunicipalityTable
    filter_class = MunicipalityListFilter
    formhelper_class = MunicipalityFilterFormHelper
    init_columns = [
        "id",
        "lau2nam",
        "nuts3nam",
        "nuts2nam",
        "ctnam",
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(MunicipalityListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [
            x for x in self.get_all_cols() if x not in self.init_columns
        ]
        context["togglable_colums"] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(
            self.request, paginate={"page": 1, "per_page": self.paginate_by}
        ).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class MunicipalityDetailView(DetailView):
    model = Municipality
    template_name = "shapes/municipality_detail.html"


class MunicipalityCreate(BaseCreateView):

    model = Municipality
    form_class = MunicipalityForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MunicipalityCreate, self).dispatch(*args, **kwargs)


class MunicipalityUpdate(BaseUpdateView):

    model = Municipality
    form_class = MunicipalityForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MunicipalityUpdate, self).dispatch(*args, **kwargs)


class MunicipalityDelete(DeleteView):
    model = Municipality
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("shapes:browse_municipality")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MunicipalityDelete, self).dispatch(*args, **kwargs)

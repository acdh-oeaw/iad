from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django_tables2 import RequestConfig

from . models import CadastralCommunity
from . tables import CadastralCommunityTable
from . filters import CadastralCommunityListFilter
from . forms import CadastralCommunityFilterFormHelper, CadastralCommunityForm

from webpage.utils import GenericListView, BaseCreateView, BaseUpdateView


class CadastralCommunityListView(GenericListView):
    model = CadastralCommunity
    table_class = CadastralCommunityTable
    filter_class = CadastralCommunityListFilter
    formhelper_class = CadastralCommunityFilterFormHelper
    init_columns = [
        'id',
        'cadcom_nam',
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(CadastralCommunityListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by
        }).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class CadastralCommunityDetailView(DetailView):
    model = CadastralCommunity
    template_name = 'shapes/cadastralcommunity_detail.html'


class CadastralCommunityCreate(BaseCreateView):

    model = CadastralCommunity
    form_class = CadastralCommunityForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CadastralCommunityCreate, self).dispatch(*args, **kwargs)


class CadastralCommunityUpdate(BaseUpdateView):

    model = CadastralCommunity
    form_class = CadastralCommunityForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CadastralCommunityUpdate, self).dispatch(*args, **kwargs)


class CadastralCommunityDelete(DeleteView):
    model = CadastralCommunity
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('shapes:browse_cadastralcommunity')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CadastralCommunityDelete, self).dispatch(*args, **kwargs)

import time
import datetime
from django.http import HttpResponse
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS, ConjunctiveGraph
from django_tables2 import SingleTableView, RequestConfig
import pandas as pd

from browsing.filters import *
from browsing.forms import *
from browsing.tables import *
try:
    from browsing.models import BrowsConf
except ImportError:
    BrowsConf = None
from archiv.models import *
from bib.models import *
from archiv.utils import *
from entities.models import Place, Institution
from entities.serializer_arche import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from charts.models import ChartConfig
from charts.views import create_payload


class GenericListView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    paginate_by = 25
    template_name = 'browsing/generic_list.html'

    def get_queryset(self, **kwargs):
        qs = super(GenericListView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model._meta.verbose_name_plural:
            context['class_name'] = "{}".format(self.model._meta.verbose_name.title())
        else:
            if self.model.__name__.endswith('s'):
                context['class_name'] = "{}".format(self.model.__name__)
            else:
                context['class_name'] = "{}s".format(self.model.__name__)
        try:
            context['get_arche_dump'] = self.model.get_arche_dump()
        except AttributeError:
            context['get_arche_dump'] = None
        try:
            context['create_view_link'] = self.model.get_createview_url()
        except AttributeError:
            context['create_view_link'] = None
        try:
            context['download'] = self.model.get_dl_url()
        except AttributeError:
            context['download'] = None
        model_name = self.model.__name__.lower()
        context['entity'] = model_name
        print(context['entity'])
        context['vis_list'] = ChartConfig.objects.filter(model_name=model_name)
        context['property_name'] = self.request.GET.get('property')
        context['charttype'] = self.request.GET.get('charttype')
        if context['charttype'] and context['property_name']:
            qs = self.get_queryset()
            chartdata = create_payload(
                context['entity'],
                context['property_name'],
                context['charttype'],
                qs
            )
            context = dict(context, **chartdata)
            print(chartdata)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenericListView, self).dispatch(*args, **kwargs)


class ReferenceListView(GenericListView):
    model = Reference
    table_class = ReferenceTable
    filter_class = ReferenceListFilter
    formhelper_class = ReferenceFormHelper
    init_columns = ['id', 'zotero_item', 'page']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ReferenceListView, self).get_context_data()
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


class MonumentProtectionListView(GenericListView):
    model = MonumentProtection
    table_class = MonumentProtectionTable
    filter_class = MonumentProtectionListFilter
    formhelper_class = MonumentProtectionFormHelper
    init_columns = ['id', 'site_id']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(MonumentProtectionListView, self).get_context_data()
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


class MonumentProtectionDl(MonumentProtectionListView):

    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get('sep', ',')
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type='text/csv')
        conf_items = list(
            BrowsConf.objects.filter(model_name='monumentprotection')
            .values_list('field_path', 'label')
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.model.objects.all().values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items]
                )
            except AssertionError:
                response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
                return response
        else:
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
            return response
        if sep == "comma":
            df.to_csv(response, sep=',', index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=';', index=False)
        elif sep == "tab":
            df.to_csv(response, sep='\t', index=False)
        else:
            df.to_csv(response, sep=',', index=False)
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        return response


class ResearchQuestionListView(GenericListView):
    model = ResearchQuestion
    table_class = ResearchQuestionTable
    filter_class = ResearchQuestionListFilter
    formhelper_class = ResearchQuestionFormHelper
    init_columns = ['id', 'question']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ResearchQuestionListView, self).get_context_data()
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


class ArchEntListView(GenericListView):
    model = ArchEnt
    table_class = ArchEntTable
    filter_class = ArchEntListFilter
    formhelper_class = ArchEntFilterFormHelper
    init_columns = ['name', 'site_id', 'ent_type']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ArchEntListView, self).get_context_data()
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


class ArchEntDl(ArchEntListView):

    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get('sep', ',')
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type='text/csv')
        conf_items = list(
            BrowsConf.objects.filter(model_name='archent').values_list('field_path', 'label')
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.model.objects.all().values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items]
                )
            except AssertionError:
                response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
                return response
        else:
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
            return response
        if sep == "comma":
            df.to_csv(response, sep=',', index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=';', index=False)
        elif sep == "tab":
            df.to_csv(response, sep='\t', index=False)
        else:
            df.to_csv(response, sep=',', index=False)
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        return response


class SiteListView(GenericListView):
    model = Site
    table_class = SiteTable
    filter_class = SiteListFilter
    formhelper_class = SiteFilterFormHelper
    init_columns = ['id', 'name', ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data()
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


class SiteDl(SiteListView):

    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get('sep', ',')
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type='text/csv')
        conf_items = list(
            BrowsConf.objects.filter(model_name='site').values_list('field_path', 'label')
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.model.objects.all().values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items]
                )
            except AssertionError:
                response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
                return response
        else:
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
            return response
        if sep == "comma":
            df.to_csv(response, sep=',', index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=';', index=False)
        elif sep == "tab":
            df.to_csv(response, sep='\t', index=False)
        else:
            df.to_csv(response, sep=',', index=False)
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        return response


class MapView(SiteListView):
    model = Site
    template_name = 'browsing/map.html'
    filter_class = SiteListFilter
    formhelper_class = SiteFilterFormHelper

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['sites'] = self.get_queryset()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MapView, self).dispatch(*args, **kwargs)


class ResearchEventListView(GenericListView):
    model = ResearchEvent
    table_class = ResearchEventTable
    filter_class = ResearchEventListFilter
    formhelper_class = ResearchEventFilterFormHelper
    init_columns = ['id', 'start_date', 'site_id', 'research_type', 'research_method']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ResearchEventListView, self).get_context_data()
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


class ResearchEventDl(ResearchEventListView):

    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get('sep', ',')
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type='text/csv')
        conf_items = list(
            BrowsConf.objects.filter(model_name='researchevent').values_list('field_path', 'label')
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.model.objects.all().values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items]
                )
            except AssertionError:
                response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
                return response
        else:
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
            return response
        if sep == "comma":
            df.to_csv(response, sep=',', index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=';', index=False)
        elif sep == "tab":
            df.to_csv(response, sep='\t', index=False)
        else:
            df.to_csv(response, sep=',', index=False)
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        return response


class AltNameListView(GenericListView):
    model = AltName
    table_class = AltNameTable
    filter_class = AltNameListFilter
    formhelper_class = AltNameFilterFormHelper
    init_columns = ['label', 'language']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(AltNameListView, self).get_context_data()
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


class PeriodListView(GenericListView):
    model = Period
    table_class = PeriodTable
    filter_class = PeriodListFilter
    formhelper_class = PeriodFilterFormHelper
    init_columns = [
        'id', 'name', 'start_date', 'start_date_latest',
        'end_date', 'end_date_latest'
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PeriodListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(
            self.request, paginate={'page': 1, 'per_page': self.paginate_by}
        ).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class AlternativeNameListView(GenericListView):
    model = AlternativeName
    table_class = AlternativeNameTable
    filter_class = AlternativeNameListFilter
    formhelper_class = AlternativeNameFilterFormHelper
    init_columns = ['id', 'name', 'part_of']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(AlternativeNameListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(
            self.request, paginate={'page': 1, 'per_page': self.paginate_by}
        ).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PersonRDFView(GenericListView):
    model = Person
    table_class = PersonTable
    template_name = 'browsing/rdflib_template.txt'
    filter_class = PersonListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='application/xml; charset=utf-8')
        filename = "places_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.rdf"'.format(filename)
        g = person_to_arche(self.get_queryset())
        get_format = self.request.GET.get('format', default='n3')
        result = g.serialize(destination=response, format=get_format)
        return response


class PlaceRDFView(GenericListView):
    model = Place
    table_class = PlaceTable
    template_name = 'browsing/rdflib_template.txt'
    filter_class = PlaceListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='application/xml; charset=utf-8')
        filename = "places_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.rdf"'.format(filename)
        g = place_to_arche(self.get_queryset())
        get_format = self.request.GET.get('format', default='n3')
        result = g.serialize(destination=response, format=get_format)
        return response


class InstitutionRDFView(GenericListView):
    model = Institution
    table_class = InstitutionTable
    template_name = 'browsing/rdflib_template.txt'
    filter_class = InstitutionListFilter
    formhelper_class = GenericFilterFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        response = HttpResponse(content_type='application/xml; charset=utf-8')
        filename = "institutions_{}".format(timestamp)
        response['Content-Disposition'] = 'attachment; filename="{}.rdf"'.format(filename)
        g = inst_to_arche(self.get_queryset())
        get_format = self.request.GET.get('format', default='n3')
        result = g.serialize(destination=response, format=get_format)
        return response


class InstitutionListView(GenericListView):
    model = Institution
    table_class = InstitutionTable
    filter_class = InstitutionListFilter
    formhelper_class = InstitutionFilterFormHelper
    init_columns = ['id', 'written_name']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PlaceListView(GenericListView):
    model = Place
    table_class = PlaceTable
    filter_class = PlaceListFilter
    formhelper_class = PlaceFilterFormHelper
    init_columns = ['id', 'name', 'lat', 'lng']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table


class PersonListView(GenericListView):
    model = Person
    table_class = PersonTable
    filter_class = PersonListFilter
    formhelper_class = PersonFilterFormHelper
    init_columns = ['id', 'written_name', 'name', 'forename']

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [x for x in self.get_all_cols() if x not in self.init_columns]
        context['togglable_colums'] = togglable_colums
        return context

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(self.request, paginate={
            'page': 1, 'per_page': self.paginate_by}).configure(table)
        default_cols = self.init_columns
        all_cols = self.get_all_cols()
        selected_cols = self.request.GET.getlist("columns") + default_cols
        exclude_vals = [x for x in all_cols if x not in selected_cols]
        table.exclude = exclude_vals
        return table

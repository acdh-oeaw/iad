import datetime
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django_tables2 import RequestConfig

from browsing.browsing_utils import BaseCreateView, BaseUpdateView, GenericListView

from .filters import (
    SkosCollectionListFilter,
    SkosConceptListFilter,
    SkosConceptSchemeListFilter,
    SkosLabelListFilter,
)
from .forms import (
    MetadataForm,
    SkosCollectionForm,
    SkosCollectionFormHelper,
    SkosConceptForm,
    SkosConceptFormHelper,
    SkosConceptSchemeForm,
    SkosConceptSchemeFormHelper,
    SkosLabelForm,
    SkosLabelFormHelper,
)
from .models import Metadata, SkosCollection, SkosConcept, SkosConceptScheme, SkosLabel
from .rdf_utils import graph_construct_qs
from .tables import (
    SkosCollectionTable,
    SkosConceptSchemeTable,
    SkosConceptTable,
    SkosLabelTable,
)

#####################################################
#   Metadata
#####################################################


class MetadataListView(ListView):
    model = Metadata
    template_name = "vocabs/metadata_list.html"


class MetadataDetailView(DetailView):
    model = Metadata
    template_name = "vocabs/metadata_detail.html"


class MetadataCreate(BaseCreateView):
    model = Metadata
    form_class = MetadataForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MetadataUpdate(BaseUpdateView):
    model = Metadata
    form_class = MetadataForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MetadataDelete(DeleteView):
    model = Metadata
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("vocabs:metadata")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


#####################################################
#   SkosCollection
#####################################################


class SkosCollectionListView(GenericListView):
    model = SkosCollection
    table_class = SkosCollectionTable
    filter_class = SkosCollectionListFilter
    formhelper_class = SkosCollectionFormHelper
    init_columns = [
        "id",
        "name",
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
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


class SkosCollectionDetailView(DetailView):
    model = SkosCollection
    template_name = "vocabs/skoscollection_detail.html"


class SkosCollectionCreate(BaseCreateView):
    model = SkosCollection
    form_class = SkosCollectionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosCollectionUpdate(BaseUpdateView):
    model = SkosCollection
    form_class = SkosCollectionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosCollectionDelete(DeleteView):
    model = SkosCollection
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("vocabs:browse_skoscollections")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


#####################################################
#   Concept
#####################################################


class SkosConceptListView(GenericListView):
    model = SkosConcept
    table_class = SkosConceptTable
    filter_class = SkosConceptListFilter
    formhelper_class = SkosConceptFormHelper
    init_columns = [
        "id",
        "pref_label",
        "broader_concept",
    ]


class SkosConceptDetailView(DetailView):
    model = SkosConcept
    template_name = "vocabs/skosconcept_detail.html"


class SkosConceptCreate(BaseCreateView):
    model = SkosConcept
    form_class = SkosConceptForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptUpdate(BaseUpdateView):
    model = SkosConcept
    form_class = SkosConceptForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptDelete(DeleteView):
    model = SkosConcept
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("vocabs:browse_vocabs")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


#####################################################
#   ConceptScheme
#####################################################


class SkosConceptSchemeListView(GenericListView):
    model = SkosConceptScheme
    table_class = SkosConceptSchemeTable
    filter_class = SkosConceptSchemeListFilter
    formhelper_class = SkosConceptSchemeFormHelper
    init_columns = [
        "id",
        "dc_title",
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
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


class SkosConceptSchemeDetailView(DetailView):
    model = SkosConceptScheme
    template_name = "vocabs/skosconceptscheme_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["concepts"] = SkosConcept.objects.filter(scheme=self.kwargs.get("pk"))
        return context


class SkosConceptSchemeCreate(BaseCreateView):
    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptSchemeUpdate(BaseUpdateView):
    model = SkosConceptScheme
    form_class = SkosConceptSchemeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosConceptSchemeDelete(DeleteView):
    model = SkosConceptScheme
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("vocabs:browse_schemes")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


###################################################
# SkosLabel
###################################################


class SkosLabelListView(GenericListView):
    model = SkosLabel
    table_class = SkosLabelTable
    filter_class = SkosLabelListFilter
    formhelper_class = SkosLabelFormHelper
    init_columns = [
        "id",
        "name",
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
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


class SkosLabelDetailView(DetailView):
    model = SkosLabel
    template_name = "vocabs/skoslabel_detail.html"


class SkosLabelCreate(BaseCreateView):
    model = SkosLabel
    form_class = SkosLabelForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosLabelUpdate(BaseUpdateView):
    model = SkosLabel
    form_class = SkosLabelForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SkosLabelDelete(DeleteView):
    model = SkosLabel
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("vocabs:browse_skoslabels")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


###################################################
# SkosConcepts download as one ConceptScheme
###################################################


class SkosConceptDL(GenericListView):
    model = SkosConcept
    table_class = SkosConceptTable
    filter_class = SkosConceptListFilter
    formhelper_class = SkosConceptFormHelper

    def render_to_response(self, context):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d-%H-%M-%S"
        )
        response = HttpResponse(content_type="application/xml; charset=utf-8")
        filename = f"download_{timestamp}"
        get_format = self.request.GET.get("format", default="pretty-xml")
        if get_format == "turtle":
            response["Content-Disposition"] = f'attachment; filename="{filename}.ttl"'
        else:
            response["Content-Disposition"] = f'attachment; filename="{filename}.rdf"'
        g = graph_construct_qs(self.get_queryset())
        g.serialize(destination=response, format=get_format)
        return response

import datetime
import time

import geopandas as gp
import pandas as pd
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.http import HttpResponse
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from shapely import wkt

from browsing.filters import (
    AlternativeNameListFilter,
    AltNameListFilter,
    ArchEntListFilter,
    InstitutionListFilter,
    MonumentProtectionListFilter,
    PeriodListFilter,
    PersonListFilter,
    PlaceListFilter,
    ReferenceListFilter,
    ResearchEventListFilter,
    ResearchQuestionListFilter,
    SiteListFilter,
)
from browsing.forms import (
    AlternativeNameFilterFormHelper,
    AltNameFilterFormHelper,
    ArchEntFilterFormHelper,
    InstitutionFilterFormHelper,
    MonumentProtectionFormHelper,
    PeriodFilterFormHelper,
    PersonFilterFormHelper,
    PlaceFilterFormHelper,
    ReferenceFormHelper,
    ResearchEventFilterFormHelper,
    ResearchQuestionFormHelper,
    SiteFilterFormHelper,
)
from browsing.tables import (
    AlternativeName,
    AlternativeNameTable,
    AltNameTable,
    ArchEntTable,
    InstitutionTable,
    MonumentProtectionTable,
    PeriodTable,
    PersonTable,
    PlaceTable,
    ReferenceTable,
    ResearchEventTable,
    ResearchQuestionTable,
    SiteTable,
)
from entities.models import Institution, Person, Place

try:
    from browsing.models import BrowsConf
except ImportError:
    BrowsConf = None
from charts.models import ChartConfig
from charts.views import create_payload
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from archiv.models import (
    AltName,
    ArchEnt,
    MonumentProtection,
    Period,
    ResearchEvent,
    ResearchQuestion,
    Site,
)
from bib.models import Reference


def flatten_df(df):
    grouped = df.groupby("internal id")
    for group in grouped:
        new = group[1]
        yield [new[x].unique().tolist() for x in new.keys()]


def serialize_as_geojson(self, model_name):
    conf_items = list(
        BrowsConf.objects.filter(model_name=model_name).values_list(
            "field_path", "label"
        )
    )
    conf_items.append(("polygon", "polygon"))
    sites_qs = self.get_queryset().distinct().exclude(polygon=None)
    if model_name == "site":
        qs = sites_qs
    elif model_name == "archent":
        qs = ArchEnt.objects.filter(site_id__in=[x.id for x in sites_qs]).exclude(
            polygon=None
        )
    elif model_name == "monumentprotection":
        qs = MonumentProtection.objects.filter(
            site_id__in=[x.id for x in sites_qs]
        ).exclude(polygon=None)
    else:
        qs = ResearchEvent.objects.filter(site_id__in=[x.id for x in sites_qs]).exclude(
            polygon=None
        )
    df = pd.DataFrame(
        list(qs.distinct().values_list(*[x[0] for x in conf_items])),
        columns=[x[1] for x in conf_items],
    )
    df_gen = flatten_df(df)
    newish = pd.DataFrame(df_gen, columns=[x[1] for x in conf_items])
    newish["geometry"] = newish.apply(
        lambda row: wkt.loads(row["polygon"][0].wkt), axis=1
    )
    # Convert non-geometry columns to string, keep geometry as-is
    non_geom_cols = [
        col for col in newish.columns if col not in ["polygon", "geometry"]
    ]
    for col in non_geom_cols:
        newish[col] = newish[col].astype("str")
    newish = newish.drop(["polygon"], axis=1)
    # Create GeoDataFrame with explicit geometry column
    gdf = gp.GeoDataFrame(newish, geometry="geometry")
    return gdf


class GenericListView(ExportMixin, SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = "filter"
    paginate_by = 10
    template_name = "browsing/generic_list.html"

    def get_queryset(self, **kwargs):
        qs = super(GenericListView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs.distinct()

    def get_table(self, **kwargs):
        table = super(GenericListView, self).get_table()
        RequestConfig(
            self.request, paginate={"page": 1, "per_page": self.paginate_by}
        ).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data()
        ct = ContentType.objects.get(model=self.model.__name__.lower()).model_class()
        try:
            ct._meta.get_field("polygon")
            poly = True
        except:  # noqa
            poly = False
        if poly:
            points = serialize(
                "geojson",
                self.get_queryset(),
                geometry_field="centroid",
                fields=(
                    "name",
                    "pk",
                ),
            )
            context["points"] = points
            shapes = serialize(
                "geojson",
                self.get_queryset(),
                geometry_field="polygon",
                fields=(
                    "name",
                    "pk",
                ),
            )
            context["shapes"] = shapes
        context["self_model_name"] = self.model.__name__.lower()
        context[self.context_filter_name] = self.filter
        context["docstring"] = "{}".format(self.model.__doc__)
        if self.model._meta.verbose_name:
            context["class_name"] = "{}".format(self.model._meta.verbose_name.title())
        else:
            context["class_name"] = "{}".format(self.model.__name__)
        try:
            context["create_view_link"] = self.model.get_createview_url()
        except AttributeError:
            context["create_view_link"] = None
        try:
            context["download"] = self.model.get_dl_url()
        except AttributeError:
            context["download"] = None
        model = self.model
        app_label = model._meta.app_label
        context["entity"] = model.__name__.lower()
        filtered_objs = ChartConfig.objects.filter(
            model_name=model.__name__.lower(), app_name=app_label
        )
        context["vis_list"] = filtered_objs
        context["property_name"] = self.request.GET.get("property")
        context["charttype"] = self.request.GET.get("charttype")
        if context["self_model_name"] == "site":
            context["enablereldl"] = True
        else:
            context["enablereldl"] = False
        if context["charttype"] and context["property_name"]:
            qs = self.get_queryset()
            chartdata = create_payload(
                context["entity"],
                context["property_name"],
                context["charttype"],
                qs,
                app_label=app_label,
            )
            context = dict(context, **chartdata)
        return context

    def render_to_response(self, context, **kwargs):
        try:
            context["shapes"]
        except KeyError:
            context["shapes"] = None
        if context["shapes"]:
            if (
                self.request.GET.get("dl-geojson", None)
                and self.get_queryset().exclude(polygon=None)
                and context["entity"]
            ):
                model_to_download = self.request.GET.get("dl-geojson", None).split(
                    "--"
                )[1]
                gdf = serialize_as_geojson(self, model_name=model_to_download)
                response = HttpResponse(gdf.to_json(), content_type="application/json")
                response["Content-Disposition"] = (
                    'attachment; filename="{}.geojson"'.format(model_to_download)
                )
                return response
            else:
                response = super(GenericListView, self).render_to_response(context)
                return response
        else:
            response = super(GenericListView, self).render_to_response(context)
            return response


class ReferenceListView(GenericListView):
    model = Reference
    table_class = ReferenceTable
    filter_class = ReferenceListFilter
    formhelper_class = ReferenceFormHelper
    init_columns = ["id", "zotero_item", "page"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ReferenceListView, self).get_context_data()
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


class MonumentProtectionListView(GenericListView):
    model = MonumentProtection
    table_class = MonumentProtectionTable
    filter_class = MonumentProtectionListFilter
    formhelper_class = MonumentProtectionFormHelper
    init_columns = ["id", "site_id"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(MonumentProtectionListView, self).get_context_data()
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


class MonumentProtectionDl(MonumentProtectionListView):
    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get("sep", ",")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d-%H-%M-%S"
        )
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type="text/csv")
        conf_items = list(
            BrowsConf.objects.filter(model_name="monumentprotection").values_list(
                "field_path", "label"
            )
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.get_queryset()
                        .distinct()
                        .values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items],
                )
            except AssertionError:
                response["Content-Disposition"] = (
                    'attachment; filename="{}.csv"'.format(filename)
                )
                return response
        else:
            response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
                filename
            )
            return response
        if sep == "comma":
            df.to_csv(response, sep=",", index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=";", index=False)
        elif sep == "tab":
            df.to_csv(response, sep="\t", index=False)
        else:
            df.to_csv(response, sep=",", index=False)
        response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
            filename
        )
        return response


class ResearchQuestionListView(GenericListView):
    model = ResearchQuestion
    table_class = ResearchQuestionTable
    filter_class = ResearchQuestionListFilter
    formhelper_class = ResearchQuestionFormHelper
    init_columns = ["id", "question"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ResearchQuestionListView, self).get_context_data()
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


class ArchEntListView(GenericListView):
    model = ArchEnt
    table_class = ArchEntTable
    filter_class = ArchEntListFilter
    formhelper_class = ArchEntFilterFormHelper
    init_columns = ["name", "site_id", "ent_type"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ArchEntListView, self).get_context_data()
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


class ArchEntDl(ArchEntListView):
    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get("sep", ",")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d-%H-%M-%S"
        )
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type="text/csv")
        conf_items = list(
            BrowsConf.objects.filter(model_name="archent").values_list(
                "field_path", "label"
            )
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.get_queryset()
                        .distinct()
                        .values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items],
                )
            except AssertionError:
                response["Content-Disposition"] = (
                    'attachment; filename="{}.csv"'.format(filename)
                )
                return response
        else:
            response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
                filename
            )
            return response
        if sep == "comma":
            df.to_csv(response, sep=",", index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=";", index=False)
        elif sep == "tab":
            df.to_csv(response, sep="\t", index=False)
        else:
            df.to_csv(response, sep=",", index=False)
        response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
            filename
        )
        return response


class SiteListView(GenericListView):
    model = Site
    table_class = SiteTable
    filter_class = SiteListFilter
    formhelper_class = SiteFilterFormHelper
    init_columns = [
        "id",
        "name",
    ]

    def get_queryset(self, **kwargs):
        user = self.request.user
        qs = super(SiteListView, self).get_queryset()
        if user.is_authenticated:
            pass
        else:
            qs = qs.exclude(site_checked_by=None).exclude(public=False)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        qs = self.get_queryset()
        context = super(SiteListView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        togglable_colums = [
            x for x in self.get_all_cols() if x not in self.init_columns
        ]
        context["togglable_colums"] = togglable_colums
        item_qs = ArchEnt.objects.filter(site_id__in=qs)
        context["shapes_archent"] = serialize(
            "geojson",
            item_qs,
            geometry_field="polygon",
            fields=("name", "pk", "identifier"),
        )
        item_qs = ResearchEvent.objects.filter(site_id__in=qs)
        context["shapes_researchevent"] = serialize(
            "geojson",
            item_qs,
            geometry_field="polygon",
            fields=("name", "pk", "identifier"),
        )
        item_qs = MonumentProtection.objects.filter(site_id__in=qs)
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


class SiteDl(SiteListView):
    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get("sep", ",")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d-%H-%M-%S"
        )
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type="text/csv")
        conf_items = list(
            BrowsConf.objects.filter(model_name="site").values_list(
                "field_path", "label"
            )
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.get_queryset()
                        .distinct()
                        .values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items],
                )
            except AssertionError:
                response["Content-Disposition"] = (
                    'attachment; filename="{}.csv"'.format(filename)
                )
                return response
        else:
            response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
                filename
            )
            return response
        if sep == "comma":
            df.to_csv(response, sep=",", index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=";", index=False)
        elif sep == "tab":
            df.to_csv(response, sep="\t", index=False)
        else:
            df.to_csv(response, sep=",", index=False)
        response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
            filename
        )
        return response


class MapView(SiteListView):
    model = Site
    template_name = "browsing/map.html"
    filter_class = SiteListFilter
    formhelper_class = SiteFilterFormHelper

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context["sites"] = self.get_queryset()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MapView, self).dispatch(*args, **kwargs)


class ResearchEventListView(GenericListView):
    model = ResearchEvent
    table_class = ResearchEventTable
    filter_class = ResearchEventListFilter
    formhelper_class = ResearchEventFilterFormHelper
    init_columns = ["id", "start_date", "site_id", "research_type", "research_method"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(ResearchEventListView, self).get_context_data()
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


class ResearchEventDl(ResearchEventListView):
    def render_to_response(self, context, **kwargs):
        sep = self.request.GET.get("sep", ",")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d-%H-%M-%S"
        )
        filename = "export_{}".format(timestamp)
        response = HttpResponse(content_type="text/csv")
        conf_items = list(
            BrowsConf.objects.filter(model_name="researchevent").values_list(
                "field_path", "label"
            )
        )
        if conf_items:
            try:
                df = pd.DataFrame(
                    list(
                        self.get_queryset()
                        .distinct()
                        .values_list(*[x[0] for x in conf_items])
                    ),
                    columns=[x[1] for x in conf_items],
                )
            except AssertionError:
                response["Content-Disposition"] = (
                    'attachment; filename="{}.csv"'.format(filename)
                )
                return response
        else:
            response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
                filename
            )
            return response
        if sep == "comma":
            df.to_csv(response, sep=",", index=False)
        elif sep == "semicolon":
            df.to_csv(response, sep=";", index=False)
        elif sep == "tab":
            df.to_csv(response, sep="\t", index=False)
        else:
            df.to_csv(response, sep=",", index=False)
        response["Content-Disposition"] = 'attachment; filename="{}.csv"'.format(
            filename
        )
        return response


class AltNameListView(GenericListView):
    model = AltName
    table_class = AltNameTable
    filter_class = AltNameListFilter
    formhelper_class = AltNameFilterFormHelper
    init_columns = ["label", "language"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(AltNameListView, self).get_context_data()
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


class PeriodListView(GenericListView):
    model = Period
    table_class = PeriodTable
    filter_class = PeriodListFilter
    formhelper_class = PeriodFilterFormHelper
    init_columns = [
        "id",
        "name",
        "start_date",
        "start_date_latest",
        "end_date",
        "end_date_latest",
        "norm_id",
    ]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PeriodListView, self).get_context_data()
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


class AlternativeNameListView(GenericListView):
    model = AlternativeName
    table_class = AlternativeNameTable
    filter_class = AlternativeNameListFilter
    formhelper_class = AlternativeNameFilterFormHelper
    init_columns = ["id", "name", "part_of"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(AlternativeNameListView, self).get_context_data()
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


class InstitutionListView(GenericListView):
    model = Institution
    table_class = InstitutionTable
    filter_class = InstitutionListFilter
    formhelper_class = InstitutionFilterFormHelper
    init_columns = ["id", "written_name"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(InstitutionListView, self).get_context_data()
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


class PlaceListView(GenericListView):
    model = Place
    table_class = PlaceTable
    filter_class = PlaceListFilter
    formhelper_class = PlaceFilterFormHelper
    init_columns = ["id", "name", "lat", "lng"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data()
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


class PersonListView(GenericListView):
    model = Person
    table_class = PersonTable
    filter_class = PersonListFilter
    formhelper_class = PersonFilterFormHelper
    init_columns = ["id", "written_name", "name", "forename"]

    def get_all_cols(self):
        all_cols = list(self.table_class.base_columns.keys())
        return all_cols

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data()
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

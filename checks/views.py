from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.gis.db.models import Union
from django.utils.decorators import method_decorator

from archiv.models import Site, ArchEnt, MonumentProtection, ResearchEvent


class GenericCheck(TemplateView):
    template_name = "checks/generic_check.html"

    def get_context_data(self, **kwargs):
        context = super(GenericCheck, self).get_context_data()
        model_name = self.kwargs["model_name"]
        context["entity"] = model_name
        if model_name in ["archent", "researchevent", "monumentprotection"]:
            entity_model = ContentType.objects.get(
                app_label="archiv", model=model_name
            ).model_class()
            context["all"] = entity_model.objects.all().count()
            context["no_site"] = entity_model.objects.filter(site_id__isnull=True)
            context["no_polygon"] = entity_model.objects.filter(polygon=None)
            context["no_nothing"] = context["no_polygon"].filter(site_id__isnull=True)
        return context


class InValidPoly(TemplateView):
    template_name = "checks/poly_invalid.html"

    def get_context_data(self, **kwargs):
        context = super(InValidPoly, self).get_context_data()
        classes = [Site, ArchEnt, MonumentProtection, ResearchEvent]
        invalid = []
        all = []
        for x in classes:
            objects = x.objects.exclude(polygon=None)
            invalid = invalid + [
                y.get_absolute_url() for y in objects if not y.polygon.valid
            ]
            all = all + [x["polygon"] for x in objects.values().values("polygon")]
        context["nr_invalid"] = len(invalid)
        context["all"] = len(all)
        context["invalid"] = invalid
        return context


class PolygonExists(TemplateView):
    template_name = "checks/poly_exists.html"

    def get_context_data(self, **kwargs):
        context = super(PolygonExists, self).get_context_data()
        model_name = self.kwargs["model_name"]
        entity_model = ContentType.objects.get(
            app_label="archiv", model=model_name
        ).model_class()
        no_poly = entity_model.objects.filter(polygon=None)
        context["no_poly"] = no_poly
        context["no_poly_count"] = no_poly.count()
        context["all"] = entity_model.objects.all().count()
        context["class"] = entity_model._meta.verbose_name
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PolygonExists, self).dispatch(*args, **kwargs)


class PolyFitsArchEnts(TemplateView):
    template_name = "checks/polyfitsarchents.html"

    def get_context_data(self, **kwargs):
        context = super(PolyFitsArchEnts, self).get_context_data()
        sites = Site.objects.exclude(polygon=None)
        errors = []
        for x in Site.objects.exclude(polygon=None):
            archs = None
            poly = None
            try:
                archs = x.has_archent.exclude(polygon=None).aggregate(
                    combined=Union("polygon")
                )
            except:  # noqa: E722
                archs = None
            if archs:
                archs = archs["combined"]
            poly = x.polygon
            if archs:
                try:
                    if Site.objects.filter(id=x.id).filter(polygon__covers=archs):
                        pass
                    else:
                        errors.append(x)
                except:  # noqa: E722
                    pass
        context["errors"] = errors
        return context

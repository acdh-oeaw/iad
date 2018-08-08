from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.gis.db.models import Union
from django.utils.decorators import method_decorator

from archiv.models import Site


class PolygonExists(TemplateView):
    template_name = "checks/poly_exists.html"

    def get_context_data(self, **kwargs):
        context = super(PolygonExists, self).get_context_data()
        model_name = self.kwargs['model_name']
        entity_model = ContentType.objects.get(app_label='archiv', model=model_name).model_class()
        no_poly = entity_model.objects.filter(polygon=None)
        context['no_poly'] = no_poly[:50]
        context['no_poly_count'] = no_poly.count()
        context['all'] = entity_model.objects.all().count()
        context['class'] = entity_model._meta.verbose_name
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
            archs = x.has_archent.exclude(polygon=None).aggregate(combined=Union('polygon'))
            archs = archs['combined']
            poly = x.polygon
            if archs:
                if Site.objects.filter(id=x.id).filter(polygon__covers=archs):
                    pass
                else:
                    errors.append(x)
        context['errors'] = errors
        return context

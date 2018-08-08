from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
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

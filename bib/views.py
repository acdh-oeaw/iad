import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from . models import ZotItem, Reference
from . forms import ReferenceForm
from django.conf import settings

# library_id = settings.Z_ID
# library_type = settings.Z_LIBRARY_TYPE
# api_key = settings.Z_API_KEY


class ReferenceListView(ListView):
    model = Reference
    template_naem = 'bib/reference_list.html'

    def get_context_data(self, **kwargs):
        context = super(ReferenceListView, self).get_context_data(**kwargs)
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
        context['count'] = self.get_queryset().count()
        return context


class BaseCreateView(CreateView):
    model = None
    form_class = None
    template_name = 'bib/generic_create.html'

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data()
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model.__name__.endswith('s'):
            context['class_name'] = "{}".format(self.model.__name__)
        else:
            context['class_name'] = "{}s".format(self.model.__name__)
        return context


class BaseUpdateView(UpdateView):
    model = None
    form_class = None
    template_name = 'archiv/generic_create.html'

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data()
        context['docstring'] = "{}".format(self.model.__doc__)
        if self.model.__name__.endswith('s'):
            context['class_name'] = "{}".format(self.model.__name__)
        else:
            context['class_name'] = "{}s".format(self.model.__name__)
        return context


class ReferenceDetailView(DetailView):
    model = Reference
    template_name = 'bib/reference_detail.html'


class ReferenceCreate(BaseCreateView):

    model = Reference
    form_class = ReferenceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReferenceCreate, self).dispatch(*args, **kwargs)


class ReferenceUpdate(BaseUpdateView):

    model = Reference
    form_class = ReferenceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReferenceUpdate, self).dispatch(*args, **kwargs)


class ReferenceDelete(DeleteView):
    model = Reference
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('browsing:browse_references')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReferenceDelete, self).dispatch(*args, **kwargs)


# def sync_zotero(request):
#     """ renders a simple template with a button to trigger sync_zotero_action function """
#     context = {}
#     return render(request, 'bib/synczotero.html', context)


# @login_required
# def update_zotitems(request):
#     """ fetches all items with higher version number then the highest stored in db """
#     context = {}
#     context["saved"] = []
#     limit = None
#     since = None
#     context["books_before"] = ZotItem.objects.all().count()
#     try:
#         first_object = ZotItem.objects.all()[:1].get()
#         since = first_object.zot_version
#     except ObjectDoesNotExist:
#         since = None

#     items = items_to_dict(library_id, library_type, api_key, limit=limit, since_version=since)
#     for x in items['bibs']:
#         temp_item = create_zotitem(x)
#         context["saved"].append(temp_item)
#     context["books_after"] = ZotItem.objects.all().count()
#     return render(request, 'bib/synczotero_action.html', context)

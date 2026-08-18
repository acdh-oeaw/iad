from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from reversion.models import Version

from .forms import (
    AltNameForm,
    ArchEntForm,
    MonumentProtectionForm,
    PeriodForm,
    ResearchEventForm,
    ResearchQuestionForm,
    SiteForm,
)
from .models import (
    AltName,
    ArchEnt,
    MonumentProtection,
    Period,
    ResearchEvent,
    ResearchQuestion,
    Site,
)


class BaseCreateView(CreateView):
    model = None
    form_class = None
    template_name = "archiv/generic_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["docstring"] = f"{self.model.__doc__}"
        context["self_model_name"] = self.model.__name__.lower()
        if self.model._meta.verbose_name:
            context["class_name"] = f"{self.model._meta.verbose_name.title()}"
        else:
            context["class_name"] = f"{self.model.__name__}"
        return context


class BaseUpdateView(UpdateView):
    model = None
    form_class = None
    template_name = "archiv/generic_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["self_model_name"] = self.model.__name__.lower()
        context["docstring"] = f"{self.model.__doc__}"
        if self.model._meta.verbose_name:
            context["class_name"] = f"{self.model._meta.verbose_name.title()}"
        else:
            context["class_name"] = f"{self.model.__name__}"
        return context


class ArchEntDetailView(DetailView):
    model = ArchEnt
    template_name = "archiv/archent_detail.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data()
        if self.object.public or user.is_authenticated:
            context["not_logged_in"] = False
        else:
            context = {}
        return context


class ArchEntCreate(BaseCreateView):
    model = ArchEnt
    form_class = ArchEntForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ArchEntUpdate(BaseUpdateView):
    model = ArchEnt
    form_class = ArchEntForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        instance = self.object

        if self.model.objects.filter(id=instance.id).filter(
            Q(ent_type__pref_label__startswith="funerary")
            | Q(ent_type__broader_concept__pref_label__startswith="funerary")
        ):
            context["no_burial"] = False
        else:
            context["no_burial"] = True

        if self.model.objects.filter(id=instance.id).filter(
            Q(ent_type__pref_label__startswith="settlement")
            | Q(ent_type__broader_concept__pref_label__startswith="settlement")
        ):
            context["no_settlement"] = False
        else:
            context["settlement"] = True

        try:
            instance = self.object
            site_poly = instance.site_id.get_geojson()
            context["site_poly"] = f"{site_poly}"
        except:  # noqa: E722
            context["site_poly"] = None
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ArchEntDelete(DeleteView):
    model = ArchEnt
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("browsing:browse_archents")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SiteDetailView(DetailView):
    model = Site
    template_name = "archiv/site_detail.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data()
        if (
            self.object.public and self.object.site_checked_by
        ) or user.is_authenticated:
            try:
                information_source = self.object.has_research_activity.order_by(
                    "start_date"
                )[0]
            except IndexError:
                information_source = None
            context["information_source"] = information_source
            context["history"] = Version.objects.get_for_object(self.object)
        else:
            context["not_logged_in"] = True
            return context
        return context


class SiteCreate(BaseCreateView):
    model = Site
    form_class = SiteForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SiteUpdate(BaseUpdateView):
    model = Site
    form_class = SiteForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SiteDelete(DeleteView):
    model = Site
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("browsing:browse_sites")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchEventDetailView(DetailView):
    model = ResearchEvent
    template_name = "archiv/researchevent_detail.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data()
        if self.object.public or user.is_authenticated:
            context["not_logged_in"] = False
        else:
            context = {}
        return context


class ResearchEventCreate(BaseCreateView):
    model = ResearchEvent
    form_class = ResearchEventForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchEventUpdate(BaseUpdateView):
    model = ResearchEvent
    form_class = ResearchEventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.object.convex_hulls:
            context["convex_hulls"] = self.object.convex_hulls
        else:
            context["convex_hulls"] = None
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchEventDelete(DeleteView):
    model = ResearchEvent
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("browsing:browse_researchevents")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AltNameDetailView(DetailView):
    model = AltName
    template_name = "archiv/altname_detail.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AltNameCreate(BaseCreateView):
    model = AltName
    form_class = AltNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AltNameUpdate(BaseUpdateView):
    model = AltName
    form_class = AltNameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AltNameDelete(DeleteView):
    model = AltName
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("browsing:browse_altnames")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PeriodDetailView(DetailView):
    model = Period
    template_name = "archiv/period_detail.html"


class PeriodCreate(BaseCreateView):
    model = Period
    form_class = PeriodForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PeriodUpdate(BaseUpdateView):
    model = Period
    form_class = PeriodForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PeriodDelete(DeleteView):
    model = Period
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("browsing:browse_periods")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchQuestionDetailView(DetailView):
    model = ResearchQuestion
    template_name = "archiv/researchquestion_detail.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchQuestionCreate(BaseCreateView):
    model = ResearchQuestion
    form_class = ResearchQuestionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchQuestionUpdate(BaseUpdateView):
    model = ResearchQuestion
    form_class = ResearchQuestionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResearchQuestionDelete(DeleteView):
    model = ResearchQuestion
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("browsing:browse_researchquestions")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MonumentProtectionDetailView(DetailView):
    model = MonumentProtection
    template_name = "archiv/monumentprotection_detail.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data()
        if self.object.public or user.is_authenticated:
            context["not_logged_in"] = False
        else:
            context = {}
        return context


class MonumentProtectionCreate(BaseCreateView):
    model = MonumentProtection
    form_class = MonumentProtectionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MonumentProtectionUpdate(BaseUpdateView):
    model = MonumentProtection
    form_class = MonumentProtectionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            instance = self.object
            site_poly = instance.site_id.get_geojson()
            context["site_poly"] = f"{site_poly}"
        except:  # noqa: E722
            context["site_poly"] = None
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MonumentProtectionDelete(DeleteView):
    model = MonumentProtection
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("browsing:browse_monumentprotections")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

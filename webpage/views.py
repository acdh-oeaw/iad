from copy import deepcopy

import requests

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import form_user_login
from .metadata import PROJECT_METADATA as PM


class ImprintView(TemplateView):
    template_name = "webpage/imprint.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            imprint_url = f"{settings.ACDH_IMPRINT_URL}{settings.REDMINE_ID}"
        except Exception as e:
            context["imprint_body"] = e
            return context
        r = requests.get(imprint_url)
        if r.status_code == 200:
            context["imprint_body"] = f"{r.text}"
        else:
            context[
                "imprint_body"
            ] = """
            On of our services is currently not available.\
            Please try it later or write an email to\
            acdh-ch-helpdesk@oeaw.ac.at; if you are service provide,\
            make sure that you provided ACDH_IMPRINT_URL and REDMINE_ID
            """
        return context


class AboutView(TemplateView):
    template_name = "webpage/about.html"


class ThesaurusView(TemplateView):
    template_name = "webpage/thesaurus.html"


if "reversion" in settings.INSTALLED_APPS:
    from reversion.models import Version

    class UserDetailView(DetailView):
        model = get_user_model()
        template_name = "webpage/user_detail.html"

        def get_context_data(self, **kwargs):
            context = super(UserDetailView, self).get_context_data()
            current_user = self.kwargs["pk"]
            versions = Version.objects.filter(revision__user__id=current_user)
            versions = list(set([x.object for x in versions]))
            rows = []
            for x in versions:
                row = []
                row.append(x)
                try:
                    row.append(x._meta.verbose_name)
                except AttributeError:
                    row.append("no type")
                rows.append(row)
            context["versions"] = rows
            context["amount"] = len(rows)
            return context

        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
            return super(UserDetailView, self).dispatch(*args, **kwargs)

else:
    pass


class GenericWebpageView(TemplateView):
    template_name = "webpage/index.html"

    def get_template_names(self):
        template_name = "webpage/{}.html".format(self.kwargs.get("template", "index"))
        try:
            loader.select_template([template_name])
            template_name = "webpage/{}.html".format(
                self.kwargs.get("template", "index")
            )
        except:  # noqa:
            template_name = "webpage/index.html"
        return [template_name]


#################################################################
#               views for login/logout                          #
#################################################################


def user_login(request):
    if request.method == "POST":
        form = form_user_login(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", "/"))
            return HttpResponse("user does not exist")
    else:
        form = form_user_login()
        return render(request, "webpage/user_login.html", {"form": form})


def user_logout(request):
    logout(request)
    return render(request, "webpage/user_logout.html")


def project_info(request):
    """
    returns a dict providing metadata about the current project
    """

    info_dict = deepcopy(PM)

    if request.user.is_authenticated:
        pass
    else:
        del info_dict["matomo_id"]
        del info_dict["matomo_url"]
    info_dict["base_tech"] = "django"
    info_dict["framework"] = "djangobaseproject"
    return JsonResponse(info_dict)

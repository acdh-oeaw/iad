from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext, loader
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . forms import form_user_login
from archiv.models import Site, ArchEnt, ResearchEvent, MonumentProtection


if 'reversion' in settings.INSTALLED_APPS:
    from reversion.models import Version

    class UserDetailView(DetailView):
        model = get_user_model()
        template_name = 'webpage/user_detail.html'

        def get_context_data(self, **kwargs):
            context = super(UserDetailView, self).get_context_data()
            current_user = self.kwargs['pk']
            versions = Version.objects.filter(revision__user__id=current_user)[:500]
            context['versions'] = versions
            return context

        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
            return super(UserDetailView, self).dispatch(*args, **kwargs)
else:
    pass


class GenericWebpageView(TemplateView):
    template_name = 'webpage/index.html'

    def get_context_data(self, **kwargs):
        context = super(GenericWebpageView, self).get_context_data()
        context['points'] = Site.get_points()
        context['shapes'] = Site.get_shapes()
        context['shapes_archent'] = ArchEnt.get_shapes()
        context['shapes_archent'] = ArchEnt.get_shapes()
        context['shapes_researchevent'] = ResearchEvent.get_shapes()
        context['shapes_monumentprotection'] = MonumentProtection.get_shapes()
        return context

    def get_template_names(self):
        template_name = "webpage/{}.html".format(self.kwargs.get("template", 'index'))
        try:
            loader.select_template([template_name])
            template_name = "webpage/{}.html".format(self.kwargs.get("template", 'index'))
        except Exception as e:
            template_name = "webpage/index.html"
        return [template_name]


#################################################################
#               views for login/logout                          #
#################################################################

def user_login(request):
    if request.method == 'POST':
        form = form_user_login(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            return HttpResponse('user does not exist')
    else:
        form = form_user_login()
        return render(request, 'webpage/user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render_to_response('webpage/user_logout.html')

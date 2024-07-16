from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView
from reversion.models import Version


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "browsing/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        current_user = self.kwargs["pk"]
        versions = Version.objects.filter(revision__user__id=current_user)
        context["versions"] = versions
        return context

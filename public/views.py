from django.shortcuts import render

from browsing.views import SiteListView


class PublicSiteListView(SiteListView):

    def get_queryset(self, **kwargs):
        qs = super(PublicSiteListView, self).get_queryset().exclude(site_checked_by=None)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

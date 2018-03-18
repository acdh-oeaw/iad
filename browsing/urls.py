from django.conf.urls import url
from . import views

app_name = 'browsing'

urlpatterns = [
    url(r'archivaltnames/$', views.AltNameListView.as_view(), name='browse_archivaltnames'),
    url(r'places/$', views.PlaceListView.as_view(), name='browse_places'),
    url(r'places-rdf/$', views.PlaceRDFView.as_view(), name='rdf_places'),
    url(r'altnames/$', views.AlternativeNameListView.as_view(), name='browse_altnames'),
    url(r'persons/$', views.PersonListView.as_view(), name='browse_persons'),
    url(r'persons-rdf/$', views.PersonRDFView.as_view(), name='rdf_persons'),
    url(r'institutions/$', views.InstitutionListView.as_view(), name='browse_institutions'),
    url(r'institutions-rdf/$', views.InstitutionRDFView.as_view(), name='rdf_institutions'),
    url(r'periods/$', views.PeriodListView.as_view(), name='browse_periods'),
    url(r'researchevents/$', views.ResearchEventListView.as_view(), name='browse_researchevents'),
    url(r'sites/$', views.SiteListView.as_view(), name='browse_sites'),
    url(r'archents/$', views.ArchEntListView.as_view(), name='browse_archents'),
]

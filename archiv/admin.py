from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import *

admin.site.register(Site, LeafletGeoAdmin)
admin.site.register(ArchEnt, LeafletGeoAdmin)
admin.site.register(AltName)
admin.site.register(ResearchEvent, LeafletGeoAdmin)
admin.site.register(Period, LeafletGeoAdmin)

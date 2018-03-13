from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Site, Settlement, AltName, Period, ResearchEvent, Cemetery

admin.site.register(Site, LeafletGeoAdmin)
admin.site.register(Settlement, LeafletGeoAdmin)
admin.site.register(AltName)
admin.site.register(ResearchEvent, LeafletGeoAdmin)
admin.site.register(Period, LeafletGeoAdmin)
admin.site.register(Cemetery, LeafletGeoAdmin)

from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Municipality


class MunicipalityAdmin(LeafletGeoAdmin):
    list_display = (
        'saunam',
        'lau2nam',
        'nuts3nam',
        'nuts2nam',
        'ctnam'
    )
    list_filter = [
        'ctnam',
    ]
    search_fields = [
        'saunam',
        'lau2nam',
        'nuts3nam',
    ]


admin.site.register(Municipality, MunicipalityAdmin)

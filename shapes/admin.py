from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from .models import CadastralCommunity


class CadastralCommunityAdmin(LeafletGeoAdmin):
    list_display = (
        'cadcom_nam',
        'nuts2_name',
        'nuts3_name',
    )
    list_filter = [
        'nuts2_name',
        'nuts3_name',
    ]
    search_fields = [
        'cadcom_nam',
        'nuts2_name',
        'nuts3_name',
    ]


admin.site.register(CadastralCommunity, CadastralCommunityAdmin)

from django.contrib.gis import admin
from reversion.admin import VersionAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import *


@admin.register(AltName)
class AltNameAdmin(VersionAdmin):
    pass


@admin.register(Site)
class SiteAdmin(VersionAdmin):
    pass


@admin.register(Period)
class PeriodAdmin(VersionAdmin):
    pass


@admin.register(ResearchQuestion)
class ResearchQuestionAdmin(VersionAdmin):
    pass


@admin.register(ResearchEvent)
class ResearchEventAdmin(VersionAdmin):
    pass


@admin.register(ArchEnt)
class ArchEntAdmin(VersionAdmin):
    pass


@admin.register(MonumentProtection)
class MonumentProtectionAdmin(VersionAdmin):
    pass

from django.contrib import admin
from .models import ZotItem, Reference


class ZotItemAdmin(admin.ModelAdmin):
    search_fields = [
        'zot_key',
        'zot_creator',
        'zot_date',
        'zot_version'
    ]
    list_display = [
        'zot_key',
        'zot_creator',
        'zot_date',
        'zot_version'
    ]


class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ['id', 'zotero_item', 'page']
    list_display = ['id', 'zotero_item', 'page']


admin.site.register(ZotItem, ZotItemAdmin)
admin.site.register(Reference, ReferenceAdmin)

# Register your models here.

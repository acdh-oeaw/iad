from django.contrib import admin

from .models import AlternativeName, Place

admin.site.register(Place)
admin.site.register(AlternativeName)

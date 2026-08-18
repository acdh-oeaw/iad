from django.contrib import admin

from .models import Metadata, SkosConcept, SkosConceptScheme, SkosLabel, SkosNamespace

admin.site.register(Metadata)
admin.site.register(SkosLabel)
admin.site.register(SkosConcept)
admin.site.register(SkosConceptScheme)
admin.site.register(SkosNamespace)

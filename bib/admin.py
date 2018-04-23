from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    search_fields = [
        'zoterokey', 'item_type', 'author', 'title', 'publication_title',
        'publication_year', 'isbn', 'url'
    ]
    list_display = [
        'zoterokey', 'item_type', 'author', 'title', 'publication_title',
        'publication_year', 'isbn', 'url'
    ]


class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ['id', 'zotero_item', 'page_number']
    list_display = ['id', 'zotero_item', 'page_number']


admin.site.register(Book, BookAdmin)

# Register your models here.

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


admin.site.register(Book, BookAdmin)

# Register your models here.

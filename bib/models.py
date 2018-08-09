# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.conf import settings

from pyzotero import zotero

library_id = settings.Z_ID
library_type = settings.Z_LIBRARY_TYPE
api_key = settings.Z_API_KEY


def fetch_bibtex(zot_key):
    """ fetches the bibtex dict of the passed in key """
    result = {}
    zot = zotero.Zotero(library_id, library_type, api_key)
    try:
        result['bibtex'] = zot.item(zot_key, format='bibtex').entries_dict
        result['error'] = None
    except Exception as e:
        result['bibtex'] = None
        result['error'] = "{}".format(e)

    return result


class ZotItem(models.Model):

    """ Stores main bibliographic information of a Zotero Item """

    zot_key = models.CharField(
        max_length=20, primary_key=True, verbose_name='key',
        help_text="The Zotero Item Key"
    )
    zot_creator = models.TextField(
        blank=True, verbose_name="creators",
        help_text="Stores all information from zoteros 'creators' field."
    )
    zot_date = models.TextField(
        blank=True, verbose_name="date",
        help_text="Stores all information from zoteros 'date' field."
    )
    zot_item_type = models.TextField(
        blank=True, verbose_name="itemType",
        help_text="Stores all information from zoteros 'itemType' field."
    )
    zot_title = models.TextField(
        blank=True, verbose_name="title",
        help_text="Stores all information from zoteros 'title' field."
    )
    zot_pub_title = models.TextField(
        blank=True, verbose_name="publicationTitle",
        help_text="Stores all information from zoteros 'publicationTitle' field."
    )
    date_modified = models.DateTimeField(
        blank=True, null=True, verbose_name="dateModified",
        help_text="Stores all information from zoteros 'publicationTitle' field."
    )
    zot_pages = models.TextField(
        blank=True, verbose_name="pages",
        help_text="Stores all information from zoteros 'pages' field."
    )
    zot_version = models.IntegerField(
        blank=True, null=True, verbose_name="version",
        help_text="Stores all information from zoteros 'pages' field."
    )
    zot_html_link = models.CharField(
        blank=True, verbose_name="selflink html", max_length=500,
        help_text="Stores all information from zoteros 'selflink' field."
    )
    zot_api_link = models.CharField(
        blank=True, verbose_name="selflink api", max_length=500,
        help_text="Stores all information from zoteros self api link field."
    )
    zot_bibtex = models.TextField(
        blank=True, verbose_name="bibtex",
        help_text="Stores the item's bibtex representation."
    )

    class Meta:
        ordering = ['-zot_version']

    def __str__(self):
        if self.zot_bibtex:
            return "{}".format(self.zot_bibtex)
        elif self.zot_title and self.zot_creator and self.zot_pub_title and self.zot_date:
            return "title: {}; pub-title: {}; creator(s): {}; year: {}".format(
                self.zot_title, self.zot_pub_title, self.zot_creator, self.zot_date
            )
        elif self.zot_title and self.zot_creator and self.zot_pub_title:
            return "title: {}; pub-title: {}; creator(s): {}; year: no date provided".format(
                self.zot_title, self.zot_pub_title, self.zot_creator
            )
        elif self.zot_creator and self.zot_pub_title:
            return "title: no title provided;\
            pub-title: {}; creator(s): {}; year: no date provided".format(
                self.zot_pub_title, self.zot_creator
            )
        else:
            return "{}".format(self.zot_key)

    def save(self, get_bibtex=False, *args, **kwargs):
        if get_bibtex:
            bibtex = fetch_bibtex(self.zot_key)
            if bibtex['bibtex']:
                self.zot_bibtex = "{}".format(bibtex['bibtex'])
                self.save()
            else:
                pass
            super(ZotItem, self).save(*args, **kwargs)
        else:
            super(ZotItem, self).save(*args, **kwargs)

    def get_zotero_url(self):
        "Returns the objects URL pointing to its Zotero entry"
        if self.zot_html_link:
            return self.zot_html_link
        else:
            return None


class Reference(models.Model):
    """Contains a precise bibliographic reference"""
    zotero_item = models.ForeignKey(
        ZotItem, blank=True, null=True,
        verbose_name="Zotero Item",
        help_text="Select the zotero item you would like to quote",
        related_name="has_references",
        on_delete=models.SET_NULL
    )
    page = models.CharField(
        max_length=250, blank=True, null=True,
        verbose_name="Page Number",
        help_text="Page Number"
    )

    class Meta:
        ordering = ['-id']

    @classmethod
    def get_listview_url(self):
        return reverse('bib:browse_references')

    @classmethod
    def get_createview_url(self):
        return reverse('bib:reference_create')

    def get_next(self):
        next = Reference.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Reference.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'bib:reference_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        try:
            return "{}, {}".format(self.zotero_item, self.page)
        except:
            return "{}".format(self.id)

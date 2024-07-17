import sys
import requests
from django.conf import settings
from django.core.management.base import NoArgsCommand

from bib.models import ZotItem


Z_USER_ID = settings.Z_USER_ID
Z_COLLECTION = settings.Z_COLLECTION
Z_API_KEY = settings.Z_API_KEY


class Command(NoArgsCommand):
    help = "a simple script to sync defc-db with zotero"

    def handle_noargs(self, **options):
        root = "https://api.zotero.org/users/"
        params = "{}/collections/{}/items/top?v=3&key={}".format(
            Z_USER_ID, Z_COLLECTION, Z_API_KEY
        )
        url = root + params + "&sort=dateModified&limit=100"
        try:
            r = requests.get(url)
        except:  # noqa: E722
            sys.exit("aa! errors! The API didn´t response with a proper json-file")

        response = r.json()

        failed = []
        saved = []
        for x in response:
            NewZotItem = ZotItem(
                zoterokey=x["data"]["key"],
                item_type=x["data"]["itemType"],
                author=x["data"]["creators"][0]["name"],
                title=x["data"]["title"],
                short_title=x["data"]["shortTitle"],
            )
            try:
                NewZotItem.save()
                saved.append(x["data"])
            except:  # noqa: E722
                failed.append(x["data"])
        print("saved: {} objects \nfailed: {} objects".format(len(saved), len(failed)))

import json

from django.http import JsonResponse
from . models import Site


def site_geojson(request):

    return JsonResponse(json.loads(Site.get_shapes()))

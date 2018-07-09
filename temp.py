# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class Municipality(models.Model):
    sau_id = models.FloatField()
    saunam = models.CharField(max_length=254)
    lau2_id = models.CharField(max_length=12)
    lau2nam = models.CharField(max_length=254)
    nuts3cod = models.CharField(max_length=254)
    nuts3nam = models.CharField(max_length=254)
    nuts2cod = models.CharField(max_length=254)
    nuts2nam = models.CharField(max_length=254)
    ctcod = models.CharField(max_length=254)
    ctnam = models.CharField(max_length=254)
    ctalt = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for Municipality model
municipality_mapping = {
    'sau_id': 'SAU_ID',
    'saunam': 'SAUnam',
    'lau2_id': 'LAU2_ID',
    'lau2nam': 'LAU2nam',
    'nuts3cod': 'NUTS3cod',
    'nuts3nam': 'NUTS3nam',
    'nuts2cod': 'NUTS2cod',
    'nuts2nam': 'NUTS2nam',
    'ctcod': 'CTcod',
    'ctnam': 'CTnam',
    'ctalt': 'CTalt',
    'geom': 'MULTIPOLYGON',
}

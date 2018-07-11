from django.urls import reverse
from django.core.serializers import serialize
from django.contrib.gis.db import models


class Municipality(models.Model):
    sau_id = models.FloatField()
    saunam = models.CharField(
        blank=True, max_length=254
    )
    lau2_id = models.CharField(
        blank=True, max_length=254
    )
    lau2nam = models.CharField(
        blank=True, max_length=254
    )
    nuts3cod = models.CharField(
        blank=True, max_length=254
    )
    nuts3nam = models.CharField(
        blank=True, max_length=254
    )
    nuts2cod = models.CharField(
        blank=True, max_length=254
    )
    nuts2nam = models.CharField(
        blank=True, max_length=254
    )
    ctcod = models.CharField(
        blank=True, max_length=254
    )
    ctnam = models.CharField(
        blank=True, max_length=254
    )
    ctalt = models.CharField(
        blank=True, max_length=254
    )
    geom = models.MultiPolygonField(blank=True, null=True, srid=4326)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.saunam and self.lau2nam:
            name = "{} ({})".format(self.saunam, self.lau2nam)
        else:
            name = "{}".format(self.lau2nam)
        return "{}, {}".format(name, self.nuts3nam)

    def get_absolute_url(self):
        return reverse(
            'shapes:municipality_detail', kwargs={'pk': self.id}
        )

    def get_geojson(self):
        geojson = serialize(
            'geojson', Municipality.objects.filter(id=self.id),
            geometry_field='geom',
            fields=('saunam', 'lau2nam', 'nuts3nam', 'nuts2nam')
        )
        return geojson


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

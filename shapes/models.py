from django.contrib.gis.db import models
from django.core.serializers import serialize
from django.urls import reverse


class Municipality(models.Model):
    lau2_id = models.CharField(blank=True, max_length=254)
    lau2nam = models.CharField(blank=True, max_length=254)
    nuts3cod = models.CharField(blank=True, max_length=254)
    nuts3nam = models.CharField(blank=True, max_length=254)
    nuts2cod = models.CharField(blank=True, max_length=254)
    nuts2nam = models.CharField(blank=True, max_length=254)
    ctcod = models.CharField(blank=True, max_length=254)
    ctnam = models.CharField(blank=True, max_length=254)
    ctalt = models.CharField(blank=True, max_length=254)
    geom = models.MultiPolygonField(blank=True, null=True, srid=4326)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        name = f"{self.lau2nam}"
        return f"{name}, {self.nuts3nam}"

    def get_absolute_url(self):
        return reverse("shapes:municipality_detail", kwargs={"pk": self.id})

    def get_geojson(self):
        geojson = serialize(
            "geojson",
            Municipality.objects.filter(id=self.id),
            geometry_field="geom",
            fields=("saunam", "lau2nam", "nuts3nam", "nuts2nam"),
        )
        return geojson


# Auto-generated `LayerMapping` dictionary for Municipality model
municipality_mapping = {
    "lau2_id": "LAU2_ID",
    "lau2nam": "LAU2nam",
    "nuts3cod": "NUTS3cod",
    "nuts3nam": "NUTS3nam",
    "nuts2cod": "NUTS2cod",
    "nuts2nam": "NUTS2nam",
    "ctcod": "CTcod",
    "ctnam": "CTnam",
    "ctalt": "CTalt",
    "geom": "MULTIPOLYGON",
}

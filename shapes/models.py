from django.urls import reverse
from django.core.serializers import serialize
from django.contrib.gis.db import models


class CadastralCommunity(models.Model):
    cadcom_num = models.BigIntegerField(
        blank=True, null=True
    )
    cadcom_nam = models.CharField(
        max_length=254, blank=True, null=True
    )
    cadcom_alt = models.CharField(
        max_length=254, blank=True, null=True
    )
    lau2_muni_field = models.BigIntegerField(
        blank=True, null=True
    )
    lau2_mun_1 = models.CharField(
        max_length=254, blank=True, null=True
    )
    polbez_num = models.BigIntegerField(
        blank=True, null=True
    )
    polbez_nam = models.CharField(
        max_length=254, blank=True, null=True
    )
    nuts3_code = models.CharField(
        max_length=254, blank=True, null=True
    )
    nuts3_name = models.CharField(
        max_length=254, blank=True, null=True
    )
    bundesland = models.BigIntegerField(
        blank=True, null=True
    )
    nuts2_name = models.CharField(
        max_length=254, blank=True, null=True
    )
    nuts2_code = models.CharField(
        max_length=254, blank=True, null=True
    )
    state_code = models.CharField(
        max_length=254, blank=True, null=True
    )
    state_name = models.CharField(
        max_length=254, blank=True, null=True
    )
    state_altn = models.CharField(
        max_length=254, blank=True, null=True
    )
    geom = models.MultiPolygonField(blank=True, null=True)

    def __str__(self):
        if self.nuts3_name and self.cadcom_nam and self.state_name:
            return "{} >> {} ({})".format(
                self.cadcom_nam, self.nuts3_name, self.state_name
            )

    def __str__(self):
        return "{}".format(self.id)

    def get_absolute_url(self):
        return reverse(
            'shapes:cadastralcommunity_detail', kwargs={'pk': self.id}
        )

    @classmethod
    def get_listview_url(self):
        return reverse('shapes:browse_cadastralcommunity')

    @classmethod
    def get_createview_url(self):
        return reverse('shapes:cadastralcommunity_create')

    def get_next(self):
        next = None
        if next:
            return None
        return False

    def get_prev(self):
        prev = None
        if prev:
            return None
        return False

    def get_geojson(self):
        geojson = serialize(
            'geojson', CadastralCommunity.objects.filter(id=self.id),
            geometry_field='geom',
            fields=('cadcom_nam', 'cadcom_num',)
        )
        return geojson


# Auto-generated `LayerMapping` dictionary for CadastralCommunity model
cadastralcommunity_mapping = {
    'cadcom_num': 'CadCom_num',
    'cadcom_nam': 'CadCom_nam',
    'cadcom_alt': 'CadCom_alt',
    # 'lau2_muni_field': 'LAU2_Muni_',
    # 'lau2_mun_1': 'LAU2_Mun_1',
    # 'polbez_num': 'PolBez_num',
    # 'polbez_nam': 'PolBez_nam',
    'nuts3_code': 'NUTS3_code',
    'nuts3_name': 'NUTS3_name',
    # 'bundesland': 'Bundesland',
    # 'nuts2_name': 'NUTS2_name',
    # 'nuts2_code': 'NUTS2_code',
    'state_code': 'STATE_code',
    'state_name': 'STATE_name',
    'state_altn': 'STATE_altn',
    'geom': 'MULTIPOLYGON',
}

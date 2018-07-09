import django_tables2 as tables
from django_tables2.utils import A
from . models import *


class MunicipalityTable(tables.Table):
    cadcom_nam = tables.LinkColumn(
        'shapes:municipality_detail',
        args=[A('pk')], verbose_name='Name'
    )

    class Meta:
        model = Municipality
        sequence = ('cadcom_nam',)
        attrs = {"class": "table table-responsive table-hover"}

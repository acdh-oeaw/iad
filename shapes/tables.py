import django_tables2 as tables
from django_tables2.utils import A
from . models import *


class MunicipalityTable(tables.Table):
    id = tables.LinkColumn(
        'shapes:municipality_detail',
        args=[A('pk')], verbose_name='ID'
    )

    class Meta:
        model = Municipality
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}

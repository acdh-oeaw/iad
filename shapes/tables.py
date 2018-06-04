import django_tables2 as tables
from django_tables2.utils import A
from . models import *


class CadastralCommunityTable(tables.Table):
    cadcom_nam = tables.LinkColumn(
        'shapes:cadastralcommunity_detail',
        args=[A('pk')], verbose_name='Name'
    )

    class Meta:
        model = CadastralCommunity
        sequence = ('cadcom_nam',)
        attrs = {"class": "table table-responsive table-hover"}

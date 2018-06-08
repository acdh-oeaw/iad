import os
from django.contrib.gis.utils import LayerMapping
from . models import CadastralCommunity, cadastralcommunity_mapping

cc_shps = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 'data', 'AT', 'AT.shp')
)


def import_shapes(verbose=True):
    lm = LayerMapping(
        CadastralCommunity, cc_shps, cadastralcommunity_mapping,
        transform=True, encoding='utf-8',
    )
    lm.save(strict=True, verbose=verbose)

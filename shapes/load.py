import os
from django.contrib.gis.utils import LayerMapping
from .models import Municipality, municipality_mapping

cc_shps = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "data", "LAU_NUTS_IAD_v3.shp")
)


def import_shapes(verbose=True):
    lm = LayerMapping(
        Municipality,
        cc_shps,
        municipality_mapping,
        transform=True,
        encoding="utf-8",
    )
    lm.save(strict=True, verbose=False)

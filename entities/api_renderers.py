import json
from rest_framework import renderers


class GeoJsonRenderer(renderers.BaseRenderer):
    media_type = "text/json"
    format = "geojson"

    def render(self, data, media_type=None, renderer_context=None):
        geojson_start = """{"type": "FeatureCollection","features": """
        geolist = []
        for x in data:
            if x:
                geolist.append(x)
            else:
                pass
        geojson_end = "}"
        geolist = json.dumps(geolist)
        geojson = f"{geojson_start}{geolist}{geojson_end}"
        return geojson

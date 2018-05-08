from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Site


class SiteSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Site
        geo_field = "polygon"

        fields = (
            'id',
            'identifier',
            'name',
        )

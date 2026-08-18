from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import ArchEnt, Site


class SiteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Site
        geo_field = "polygon"

        fields = (
            "id",
            "identifier",
            "name",
        )


class ArchEntSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ArchEnt
        geo_field = "polygon"

        fields = (
            "id",
            "site_id",
            "identifier",
            "name",
        )

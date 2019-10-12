from .models import Site
from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer

class SitesSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = Site
        geo_field = 'location'
        fields = '__all__'

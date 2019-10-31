from .models import Site, SiteAgency, Agency, SiteIdentifiers, IdentifierType, ApiInfo, ApiConformance
from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer


class ApiInfoSerialiser(serializers.ModelSerializer):

    class Meta:
        model = ApiInfo
        #TODO add links to other pages into the serialiser
        fields = ['title', 'description']


class ApiConformanceSerialiser(serializers.ModelSerializer):

    class Meta:
        model = ApiConformance
        # TODO change so matches wfs3 requirements
        fields = ['name', 'url']


class AgencyDetailSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Agency
        fields = ['agency_name', 'website']


class AgencySerialiser(serializers.ModelSerializer):
    agency = AgencyDetailSerialiser()

    class Meta:
        model = SiteAgency
        fields = ['agency', 'from_date', 'to_date']
        #depth = 1


class IdentifierTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = IdentifierType
        fields = ['identifier_name']


class IdentifierSerialiser(serializers.ModelSerializer):
    identifier_type = IdentifierTypeSerialiser()
    class Meta:
        model = SiteIdentifiers
        fields = ['identifier', 'identifier_type']


class SitesSerializer(GeoFeatureModelSerializer):
    """ A class to serialize sites as GeoJSON compatible data """
    site_agencies = AgencySerialiser(many=True, read_only=True)
    site_identifiers = IdentifierSerialiser(many=True)

    class Meta:
        model = Site
        geo_field = 'location'
        fields = ['id', 'site_name', 'location', 'site_identifiers', 'site_agencies'] #'ident_type_to_site',

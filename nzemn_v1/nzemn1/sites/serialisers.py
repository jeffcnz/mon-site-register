from .models import Site, SiteAgency, Agency, SiteIdentifiers, IdentifierType
from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer


class AgencyDetailSerialiser(serializers.ModelSerializer):
    #maintained_site = AgencySiteSerialiser(many=True, read_only=True)

    class Meta:
        model = Agency
        #fields = ['agency_name', 'website', 'maintained_site']
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
    #identifier = IdentifierSiteSerialiser(many=True, read_only=True)
    #ident_type_to_site = IdentifierSiteSerialiser()
    class Meta:
        model = SiteIdentifiers
        fields = ['identifier', 'identifier_type']
        #exclude = ['id']
        #depth = 1
        #fields = ['identifier_n', 'identifier']
        #fields = ['identifier_name']


class SitesSerializer(GeoFeatureModelSerializer):
    """ A class to serialize sites as GeoJSON compatible data """
    site_agencies = AgencySerialiser(many=True, read_only=True)
    #identifiers = IdentifierTypeSerialiser(many=True, read_only=True)
    #ident_type_to_site = IdentifierSerialiser(many=True)
    #site_to_ident_type = IdentifierSerialiser(many=True)
    site_identifiers = IdentifierSerialiser(many=True)

    class Meta:
        model = Site
        geo_field = 'location'
        #fields = '__all__'
        fields = ['site_name', 'location', 'site_identifiers', 'site_agencies'] #'ident_type_to_site',

from .models import Site, SiteAgency, Agency, SiteIdentifiers, IdentifierType, AboutBody, About, ApiInfo, ApiConformance
from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer


class AboutBodySerialiser(serializers.ModelSerializer):

    class Meta:
        model = AboutBody
        fields = ['heading','text']


class AboutSerialiser(serializers.ModelSerializer):
    about_body = AboutBodySerialiser(many=True)
    type = serializers.CharField(default='about')

    class Meta:
        model = About
        fields = ['type', 'title', 'about_body', 'licence', 'author']


class ApiInfoSerialiser(serializers.ModelSerializer):
    type = serializers.CharField(default='api_info')
    class Meta:
        model = ApiInfo
        #TODO add links to other pages into the serialiser
        fields = ['type', 'title', 'description']


class ApiConformanceSerialiser(serializers.ModelSerializer):

    class Meta:
        model = ApiConformance
        # TODO change so matches wfs3 requirements
        fields = ['name', 'url']



#class ApiConformanceSerialiser(serializers.Serializer):
    #type = serializers.CharField(default='conformance')
    #conformsTo = ApiConformanceListSerialiser(many=True)
    #class Meta:
        #model = ApiConformance
        # TODO change so matches wfs3 requirements
        #fields = ['type', 'conformsTo']


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
        fields = ['id', 'site_name', 'location', 'site_identifiers', 'site_agencies'] #'ident_type_to_site',

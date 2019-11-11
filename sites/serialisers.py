from django.db import transaction

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


class AgencySerialiser(serializers.ModelSerializer):

    class Meta:
        model = Agency
        fields = ['agency_name', 'website']
        #read_only_fields = ['agency_name', 'website']


class SiteAgencySerialiser(serializers.ModelSerializer):
    #agency = AgencySerialiser()
    agency_name = serializers.CharField(source='agency.agency_name')
    website = serializers.CharField(source='agency.website')

    class Meta:
        model = SiteAgency
        fields = ['agency_name', 'website', 'from_date', 'to_date']
        #fields = ['agency', 'from_date', 'to_date']
        #depth = 1

    # Define a custom create method for nested database
    #def create(self, validated_data):
        #agency_detail_data = validated_data.pop('agency')
    #    print("Getting to here")
    #    agencies_detail_data = validated_data.pop('agency')
    #    agency = SiteAgency.objects.create(**validated_data)
    #    agencydetail = Agency.objects.create(agency=agency, **validated_data)
        #for agency_detail_data in agencies_detail_data:
            #agencydetail = Agency.objects.create(agency=agency, **validated_data)
            #agency = SiteAgency.objects.create(**validated_data)
            #Agency.objects.create(agency=agency, **agency_detail_data)
        #agency = SiteAgency.objects.create(**validated_data)
        #Agency.objects.create(agency=agency, **agency_detail_data)
    #    return agency


class IdentifierTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = IdentifierType
        fields = ['identifier_name']
        #read_only_fields = ['identifier_name']


class SiteIdentifiersSerialiser(serializers.ModelSerializer):
    #identifier_name = serializers.StringRelatedField()
    identifier_name = serializers.CharField(source='identifier_type.identifier_name')
    #identifier_type = IdentifierTypeSerialiser()

    class Meta:
        model = SiteIdentifiers
        fields = ['identifier_name', 'identifier']
        #fields = ['identifier', 'identifier_type']

    # Define a custom create method for nested database
    #def create(self, validated_data):
    #    identifier_type_data = validated_data.pop('identifier_type')
    #    identifier = SiteIdentifiers.objects.create(**validated_data)
    #    IdentifierType.objects.create(identifier=identifier, **identifier_type_data)
    #    return identifier


class SitesSerializer(GeoFeatureModelSerializer):
    """ A class to serialize sites as GeoJSON compatible data """
    #site_agencies = AgencySerialiser(many=True, read_only=True)
    site_agencies = SiteAgencySerialiser(source="siteagency_set", many=True)
    site_identifiers = SiteIdentifiersSerialiser(source="siteidentifiers_set", many=True)

    class Meta:
        model = Site
        geo_field = 'location'
        fields = ['id', 'site_name', 'location', 'site_identifiers', 'site_agencies']

    # from https://codereview.stackexchange.com/questions/164616/django-rest-framework-manytomany-relationship-through-intermediate-model
    @transaction.atomic
    def create(self, validated_data):
        agencies_data = validated_data.pop('siteagency_set')
        identifiers_data = validated_data.pop('siteidentifiers_set')
        site = Site.objects.create(**validated_data)
        if agencies_data:
            #site_agencies = self.initial_data.get("site_agencies")
            for agency in agencies_data:
                agency_info = agency['agency']
                agency_name = agency_info['agency_name']
                from_date = agency['from_date']
                to_date = agency['to_date']
                agency_instance = Agency.objects.get(agency_name=agency_name)
                SiteAgency(site=site, agency=agency_instance, from_date=from_date, to_date=to_date).save()
        if identifiers_data:
            #site_identifiers = self.initial_data.get("site_identifiers")
            for identifier_type in identifiers_data:
                print(identifier_type)
                identifier_info = identifier_type['identifier_type']
                identifier_name = identifier_info['identifier_name']
                identifier = identifier_type['identifier']
                identifier_type_instance = IdentifierType.objects.get(identifier_name=identifier_name)
                SiteIdentifiers(site=site, identifier_type=identifier_type_instance, identifier=identifier).save()
        site.save()
        return site


    #Define a custom create method for nested data
    #def create(self, validated_data):
    #    print(validated_data)
    #    agencies_data = validated_data.pop('site_agencies')
    #    identifiers_data = validated_data.pop('site_identifiers')
    #    site = Site.objects.create(**validated_data)
    #    for agency_data in agencies_data:
            #Convert Ordered Dicts to dictionaries from https://stackoverflow.com/questions/20166749/how-to-convert-an-ordereddict-into-a-regular-dict-in-python3
            #agency_data = deep_convert_dict(agency_data)
    #        print(agency_data)
    #        agency, created = Agency.objects.get_or_create(agency_name=agency_data['agency']['agency_name'])
    #        site.agencies.add(agency, "2010-01-01")
            #siteagency = SiteAgency.objects.create(site=site, **agency_data)
        #SiteAgency.objects.create(site=site, **agency_data)
    #    for identifier_data in identifiers_data:
    #        siteidentifiers = SiteIdentifiers.objects.create(site=site, **identifier_data)
        #SiteIdentifiers.objects.create(site=site, **identifier_data)
    #    return site

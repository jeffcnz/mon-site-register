from django.db import transaction

from .models import Site, SiteAgency, Agency, SiteIdentifiers, IdentifierType, ApiInfo, ApiConformance
from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.reverse import reverse

class ApiInfoSerialiser(serializers.ModelSerializer):
    # Add a links field
    links = serializers.SerializerMethodField()

    # Define the links to add
    def get_links(self, obj):
        # Get the request objects so that full urls can be used
        request = self.context.get("request")
        # get the media type requested
        media_type = request.accepted_media_type.split(';')[0]
        # Build the links
        output_links = [
            {"href": reverse('info', request=request),
            "rel": "self",
            "type": media_type,
            "title": "This document."},
            {"href": reverse('openapi-schema', request=request),
            "rel": "service-desc",
            "type": "application/vnd.oai.openapi",
            "title": "The API definition"},
            {"href": reverse('swagger-ui', request=request),
            "rel": "service-doc",
            "type": "text/html",
            "title": "The API documentation"},
            {"href": reverse('conformance', request=request),
            "rel": "conformance",
            "type": "application/json",
            "title": "OGC API conformance classes implemented by this server"},
            {"href": reverse('collections', request=request),
            "rel": "data",
            "type": "application/json",
            "title": "Information about the feature collections"}
            ]
        return output_links #obj.get_absolute_url()

    class Meta:
        model = ApiInfo
        #TODO add links to other pages into the serialiser
        fields = ['title', 'description', 'links']


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


class SitesSerializer(GeoFeatureModelSerializer):
    """ A class to serialize sites as GeoJSON compatible data """
    #site_agencies = AgencySerialiser(many=True, read_only=True)
    site_agencies = SiteAgencySerialiser(source="siteagency_set", many=True)
    site_identifiers = SiteIdentifiersSerialiser(source="siteidentifiers_set", many=True)

    class Meta:
        model = Site
        geo_field = 'location'
        fields = ['id', 'site_name', 'location', 'site_identifiers', 'site_agencies']

    # modified from https://codereview.stackexchange.com/questions/164616/django-rest-framework-manytomany-relationship-through-intermediate-model
    @transaction.atomic
    def create(self, validated_data):
        # create subsets of the nested data
        agencies_data = validated_data.pop('siteagency_set')
        identifiers_data = validated_data.pop('siteidentifiers_set')
        # create the new site base object
        site = Site.objects.create(**validated_data)
        # check if agencies data has been provided
        if agencies_data:
            # If it has for each entry extract the data and
            # create a new instance in the through table
            for agency in agencies_data:
                agency_info = agency['agency']
                agency_name = agency_info['agency_name']
                from_date = agency['from_date']
                to_date = agency['to_date']
                agency_instance = Agency.objects.get(agency_name=agency_name)
                SiteAgency(site=site, agency=agency_instance, from_date=from_date, to_date=to_date).save()
        # check if identifiers data has been provided
        if identifiers_data:
            # If it has for each entry extract the data and
            # create a new instance in the through table
            #site_identifiers = self.initial_data.get("site_identifiers")
            for identifier_type in identifiers_data:
                identifier_info = identifier_type['identifier_type']
                identifier_name = identifier_info['identifier_name']
                identifier = identifier_type['identifier']
                identifier_type_instance = IdentifierType.objects.get(identifier_name=identifier_name)
                SiteIdentifiers(site=site, identifier_type=identifier_type_instance, identifier=identifier).save()

        # Save and return the new record
        site.save()
        return site

    def update(self, instance, validated_data):
        # Get the relevant instance from the databases
        #site = Site.objects.get(site=instance)
        # create subsets of the nested data if they exist
        try:
            agencies_data = validated_data.pop('siteagency_set')
        except:
            agencies_data = False

        try:
            identifiers_data = validated_data.pop('siteidentifiers_set')
        except:
            identifiers_data = False
        # Check if agency data has been provided
        # TODO Need to work through how to update in here as
        # multiple entries are allowed. Will need some logic regarding
        # date comparisons.  Complex
        #if agencies_data:
            # Iterate through the agencies
        #    for agency in agencies_data:
                # Extract the agency name and retrieve it's instance from the db
        #        agency_name = agency['agency']['agency_name']
        #        agency_instance = Agency.objects.get(agency_name=agency_name)
                # get the extra info (TODO check for values)
        #        from_date = agency['from_date']
        #        to_date = agency['to_date']
                # save the record in the linking table
        #        SiteAgency(site=instance, agency=agency_instance, from_date=from_date, to_date=to_date).save()
        # check if identifiers data has been provided
        if identifiers_data:
            # Iterate through the identifiers
            for identifier_type in identifiers_data:
                # Extract identifier name and get it's instance from db
                identifier_name = identifier_type['identifier_type']['identifier_name']
                identifier_type_instance = IdentifierType.objects.get(identifier_name=identifier_name)
                # get the identifier (TODO check for values)
                identifier = identifier_type['identifier']
                # get the id of the identifier type
                identifier_type_instance = IdentifierType.objects.get(identifier_name=identifier_name)
                # get or create the lookup table entry
                identifier_instance, new_object = SiteIdentifiers.objects.get_or_create(site=instance, identifier_type=identifier_type_instance)
                # update the identifier
                identifier_instance.identifier = identifier
                # save the record
                identifier_instance.save()


        #update the site record
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance

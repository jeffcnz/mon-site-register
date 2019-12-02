#from django.contrib.gis import admin

from django.contrib import admin

from django.forms.widgets import Textarea
from django.contrib.gis.db import models
from . import widgets

from sites.forms import GISEntryForm
#import nested_admin

from .models import (Site, Agency, IdentifierType,
                    SiteAgency, SiteIdentifiers, ApiInfo,
                    ApiConformance, ApiCollections, SiteAgencyMeasurement,
                    AgencyMeasurement, ObservedProperty)

#from leaflet.admin import LeafletGeoAdmin


#class OperationInline(admin.TabularInline):
#    model = SiteOperation
#    extra = 0
#class AgencyMeasurementInline(nested_admin.NestedTabularInline):
#    model = SiteAgencyMeasurement
#    sortable_field_name = 'agency_measurement'
#    extra = 0


class SiteAgencyMeasurementInline(admin.TabularInline):
    model = SiteAgencyMeasurement
    extra = 0


class SiteAgencyAdmin(admin.ModelAdmin):
    list_display = ('agency', 'site')
    list_filter = ['agency']
    search_fields = ['site__site_name']
    inlines = [SiteAgencyMeasurementInline]


class AgenciesInline(admin.TabularInline):
#class AgenciesInline(nested_admin.NestedStackedInline):
    model = SiteAgency
    #sortable_field_name = 'agency'
    extra = 0
    #inlines = [AgencyMeasurementInline]


class IdentifiersInline(admin.TabularInline):
#class IdentifiersInline(nested_admin.NestedTabularInline):
    model = SiteIdentifiers
    #sortable_field_name = 'identifier_type'
    extra = 0


class SiteAdmin(admin.ModelAdmin):
#class SiteAdmin(nested_admin.NestedModelAdmin):
    list_display = ['site_name']
    list_filter = ['agencies']
    search_fields = ['site_name']
    form = GISEntryForm

    inlines = [IdentifiersInline, AgenciesInline]


class ApiCollectionsInline(admin.TabularInline):
    model = ApiCollections
    extra = 0


class ApiConformanceInline(admin.TabularInline):
    model = ApiConformance
    extra = 0


class ApiInfoAdmin(admin.ModelAdmin):

    inlines = [ApiCollectionsInline, ApiConformanceInline]

class AgencyMeasurementAdmin(admin.ModelAdmin):
    list_display = ['agency', 'observed_property', 'agency_measurement_name']
    list_filter = ['agency', 'observed_property']
    search_fields = ['observed_property', 'agency_measurement_name']

admin.site.register(Site, SiteAdmin)
admin.site.register(Agency)
admin.site.register(IdentifierType)
#admin.site.register(SiteAgency)
#admin.site.register(SiteOperation)
#admin.site.register(SiteIdentifiers)
admin.site.register(ObservedProperty)
admin.site.register(AgencyMeasurement, AgencyMeasurementAdmin)
admin.site.register(SiteAgency, SiteAgencyAdmin)
admin.site.register(ApiInfo, ApiInfoAdmin)
#admin.site.register(ApiConformance)

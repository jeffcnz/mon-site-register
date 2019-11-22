#from django.contrib.gis import admin

from django.contrib import admin

from django.forms.widgets import Textarea
from django.contrib.gis.db import models
from . import widgets

from sites.forms import GISEntryForm

from .models import Site, Agency, IdentifierType, SiteAgency, SiteOperation, SiteIdentifiers, ApiInfo, ApiConformance, ApiCollections

#from leaflet.admin import LeafletGeoAdmin


class OperationInline(admin.TabularInline):
    model = SiteOperation
    extra = 0


class AgenciesInline(admin.TabularInline):
    model = SiteAgency
    extra = 0


class IdentifiersInline(admin.TabularInline):
    model = SiteIdentifiers
    extra = 0


class SiteAdmin(admin.ModelAdmin):

    form = GISEntryForm

    inlines = [IdentifiersInline, AgenciesInline, OperationInline]


class ApiCollectionsInline(admin.TabularInline):
    model = ApiCollections
    extra = 0


class ApiInfoAdmin(admin.ModelAdmin):

    inlines = [ApiCollectionsInline]


admin.site.register(Site, SiteAdmin)
admin.site.register(Agency)
admin.site.register(IdentifierType)
#admin.site.register(SiteAgency)
#admin.site.register(SiteOperation)
#admin.site.register(SiteIdentifiers)

admin.site.register(ApiInfo, ApiInfoAdmin)
admin.site.register(ApiConformance)

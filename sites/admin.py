#from django.contrib.gis import admin

from django.contrib import admin

from django.forms.widgets import Textarea
from django.contrib.gis.db import models
from . import widgets

from .models import Site, Agency, IdentifierType, SiteAgency, SiteOperation, SiteIdentifiers, ApiInfo, ApiConformance

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
#class SiteAdmin(admin.OSMGeoAdmin):
    #default_lon = 173.2840
    #default_lat = -41.2706
    #default_lon = 19289886.64
    #default_lat = -5052337.41

    #default_zoom = 6
    formfield_overrides = {
        #models.PointField: {'widget': Textarea}
        models.PointField: {'widget': widgets.LatLongWidget}
    }

    fieldsets = [
        (None,               {'fields': ['site_name']}),
        #('Location', {'fields': ['location'], 'classes': ['collapse']}),
        ('Location', {'fields': ['location']}),
    ]
    inlines = [IdentifiersInline, AgenciesInline, OperationInline]


admin.site.register(Site, SiteAdmin)
admin.site.register(Agency)
admin.site.register(IdentifierType)
#admin.site.register(SiteAgency)
#admin.site.register(SiteOperation)
#admin.site.register(SiteIdentifiers)

admin.site.register(ApiInfo)
admin.site.register(ApiConformance)

from django.contrib.gis import admin

from .models import Site, Agency, IdentifierType, SiteAgency, SiteOperation, SiteIdentifiers

#from leaflet.admin import LeafletGeoAdmin

class OperationInline(admin.StackedInline):
    model = SiteOperation
    extra = 0


class AgenciesInline(admin.StackedInline):
    model = SiteAgency
    extra = 0


class IdentifiersInline(admin.StackedInline):
    model = SiteIdentifiers
    extra = 0


class SiteAdmin(admin.OSMGeoAdmin):
    #default_lon = 173.2840
    #default_lat = -41.2706
    default_lon = 19289886.64
    default_lat = -5052337.41

    default_zoom = 6

    fieldsets = [
        (None,               {'fields': ['site_name']}),
        ('Location', {'fields': ['location'], 'classes': ['collapse']}),
    ]
    inlines = [IdentifiersInline, AgenciesInline, OperationInline]


admin.site.register(Site, SiteAdmin)
admin.site.register(Agency)
admin.site.register(IdentifierType)
#admin.site.register(SiteAgency)
#admin.site.register(SiteOperation)
#admin.site.register(SiteIdentifiers)

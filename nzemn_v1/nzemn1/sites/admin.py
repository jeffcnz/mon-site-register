from django.contrib import admin

from .models import Site, Agency, IdentifierType, SiteAgency, SiteOperation, SiteIdentifiers

admin.site.register(Site)
admin.site.register(Agency)
admin.site.register(IdentifierType)
admin.site.register(SiteAgency)
admin.site.register(SiteOperation)
admin.site.register(SiteIdentifiers)

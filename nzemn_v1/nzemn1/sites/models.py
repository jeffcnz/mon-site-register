#from django.db import models
from django.contrib.gis.db import models
#from django.dispatch import receiver
from django.contrib.auth.models import User, Group

from django.db.models.signals import post_save
from django.dispatch import receiver

from guardian.shortcuts import assign_perm


class ApiInfo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title


class ApiConformance(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    def __str__(self):
        return self.name


class Agency(models.Model):
    agency_name = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    site_webservices = models.ForeignKey('AgencySiteListServices', null=True, blank=True, on_delete=models.CASCADE, related_name='agency_site_lists')
    def __str__(self):
        return self.agency_name


class IdentifierType(models.Model):
    identifier_name = models.CharField(max_length=200)
    def __str__(self):
        return self.identifier_name


class Site(models.Model):
    site_name = models.CharField(max_length=200)
    location = models.PointField('site location', null=True, blank=True)
    identifiers = models.ManyToManyField(IdentifierType, through='SiteIdentifiers')
    agencies = models.ManyToManyField(Agency, through='SiteAgency')
    #operational_periods = models.ForeignKey('SiteOperation', null=True, on_delete=models.CASCADE, related_name='site_operating')
    # need to add a feature of interest, but how define???
    def __str__(self):
        return self.site_name


class SiteAgency(models.Model):
    # Check / work through the on delete actions
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_agencies')
    agency = models.OneToOneField(Agency, on_delete=models.CASCADE, related_name='agency_to_site')
    from_date = models.DateField('agency from date')
    to_date = models.DateField('agency to date', null=True, blank=True)
    #def __str__(self):
    #    return self.agency_name


class SiteOperation(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    from_date = models.DateField('operational from date')
    to_date = models.DateField('operational to date', null=True, blank=True)
    #def __str__(self):
    #    return self.from_date


class SiteIdentifiers(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_identifiers') #site_to_ident_type
    #identifier_type = models.ForeignKey(IdentifierType, on_delete=models.CASCADE, related_name='site_ident') #ident_type_to_site
    identifier_type = models.OneToOneField(IdentifierType, on_delete=models.CASCADE, related_name='ident_site') #ident_type_to_site
    identifier = models.CharField(max_length=200)

    #def __str__(self):
    #    return self.identifier_type


class AgencySiteListServices(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    service_type = models.ForeignKey('SiteServiceTypes', on_delete=models.CASCADE, related_name='site_service_types')
    service_url = models.CharField(max_length=250)


class SiteServiceTypes(models.Model):
    service_type = models.CharField(max_length=50)


@receiver(post_save, sender=Agency)
def create_agency_group(sender, instance, created, **kwargs):
    if created:
        newgroup = Group.objects.create(name=instance.agency_name)
        newgroup.save()
        assign_perm('change_agency', newgroup, newgroup)

#from django.db import models
from django.contrib.gis.db import models

class Site(models.Model):
    site_name = models.CharField(max_length=200)
    location = models.PointField('site location', null=True, blank=True)
    # need to add a feature of interest, but how define???
    def __str__(self):
        return self.site_name


class Agency(models.Model):
    agency_name = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    def __str__(self):
        return self.agency_name


class IdentifierType(models.Model):
    identifier_name = models.CharField(max_length=200)
    def __str__(self):
        return self.identifier_name


class SiteAgency(models.Model):
    # Check / work through the on delete actions
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    from_date = models.DateField('agency from date')
    to_date = models.DateField('agency to date', null=True, blank=True)


class SiteOperation(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    from_date = models.DateField('operational from date')
    to_date = models.DateField('operational to date', null=True, blank=True)


class SiteIdentifiers(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    identifier_type = models.ForeignKey(IdentifierType, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=200)

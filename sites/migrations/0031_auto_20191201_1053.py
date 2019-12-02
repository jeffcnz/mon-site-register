# Generated by Django 2.2.6 on 2019-11-30 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0030_auto_20191201_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observedproperty',
            name='observed_property_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='siteagency',
            name='from_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='agency from date'),
        ),
        migrations.AddConstraint(
            model_name='agencymeasurement',
            constraint=models.UniqueConstraint(fields=('agency', 'agency_measurement_name'), name='unique agency measurements'),
        ),
        migrations.AddConstraint(
            model_name='siteagency',
            constraint=models.UniqueConstraint(fields=('site', 'agency'), name='unique site agency'),
        ),
        migrations.AddConstraint(
            model_name='siteagencymeasurements',
            constraint=models.UniqueConstraint(fields=('site_agency', 'agency_measurement'), name='unique site agency measurement'),
        ),
    ]

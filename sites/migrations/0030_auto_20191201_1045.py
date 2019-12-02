# Generated by Django 2.2.6 on 2019-11-30 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0029_delete_siteoperation'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencyMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_measurement_name', models.CharField(max_length=200)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Agency')),
            ],
        ),
        migrations.CreateModel(
            name='ObservedProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observed_property_name', models.CharField(max_length=200)),
                ('observed_property_url', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='SiteAgencyMeasurements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_url', models.CharField(max_length=400)),
                ('meas_from', models.DateTimeField(blank=True, null=True, verbose_name='site agency measurement from date')),
                ('meas_to', models.DateTimeField(blank=True, null=True, verbose_name='site agency measurement to date')),
                ('agency_measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.AgencyMeasurement')),
                ('site_agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.SiteAgency')),
            ],
        ),
        migrations.AddField(
            model_name='agencymeasurement',
            name='observed_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.ObservedProperty'),
        ),
    ]
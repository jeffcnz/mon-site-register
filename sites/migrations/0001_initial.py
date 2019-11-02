# Generated by Django 2.2.4 on 2019-08-29 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_name', models.CharField(max_length=200)),
                ('website', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='IdentifierType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SiteOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(verbose_name='operational from date')),
                ('to_date', models.DateTimeField(verbose_name='operational to date')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='SiteIdentifiers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=200)),
                ('identifier_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.IdentifierType')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='SiteAgency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(verbose_name='agency from date')),
                ('to_date', models.DateTimeField(verbose_name='agency to date')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Agency')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
        ),
    ]
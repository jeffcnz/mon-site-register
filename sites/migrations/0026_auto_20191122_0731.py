# Generated by Django 2.2.6 on 2019-11-21 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0025_auto_20191112_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteagency',
            name='from_date',
            field=models.DateTimeField(verbose_name='agency from date'),
        ),
        migrations.AlterField(
            model_name='siteagency',
            name='to_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='agency to date'),
        ),
    ]

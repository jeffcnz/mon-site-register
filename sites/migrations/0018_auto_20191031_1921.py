# Generated by Django 2.2.4 on 2019-10-31 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0017_auto_20191028_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutbody',
            name='about',
        ),
        migrations.DeleteModel(
            name='About',
        ),
        migrations.DeleteModel(
            name='AboutBody',
        ),
    ]
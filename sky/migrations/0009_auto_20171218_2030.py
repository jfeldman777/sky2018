# Generated by Django 2.0 on 2017-12-18 17:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sky', '0008_auto_20171218_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='magicnode',
            name='sites',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True), null=True, size=None),
        ),
        migrations.AddField(
            model_name='magicnode',
            name='videos',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True), null=True, size=None),
        ),
    ]

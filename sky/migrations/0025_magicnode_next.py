# Generated by Django 2.0 on 2018-02-06 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sky', '0024_auto_20180205_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='magicnode',
            name='next',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

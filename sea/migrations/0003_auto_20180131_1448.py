# Generated by Django 2.0 on 2018-01-31 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sea', '0002_auto_20180131_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
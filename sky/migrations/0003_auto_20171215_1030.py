# Generated by Django 2.0 on 2017-12-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sky', '0002_magicnode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magicnode',
            name='video',
            field=models.FileField(null=True, upload_to='uploads/%Y/%m/%d'),
        ),
    ]

# Generated by Django 2.0 on 2018-01-10 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sky', '0017_auto_20180109_1020'),
        ('area', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='root',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sky.MagicNode'),
            preserve_default=False,
        ),
    ]

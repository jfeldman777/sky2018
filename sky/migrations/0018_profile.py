# Generated by Django 2.0 on 2018-01-27 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sky', '0017_auto_20180109_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited_at', models.DateTimeField(auto_now=True)),
                ('node_last_visited', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sky.MagicNode')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.0 on 2017-12-31 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sky', '0015_auto_20171222_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='i_am_an_expert',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='interest',
            name='i_like_the_content',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='interest',
            name='i_like_the_topic',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-01 11:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatalog',
            name='emial',
            field=models.CharField(default=django.utils.timezone.now, max_length=10000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userdatalog',
            name='phone',
            field=models.IntegerField(default=1231231231),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_userdatalog_emial_userdatalog_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdatalog',
            name='emial',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='userdatalog',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

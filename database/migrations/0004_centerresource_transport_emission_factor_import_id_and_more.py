# Generated by Django 4.2.2 on 2023-07-10 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_centerwaste_emission_factor_import_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='centerresource',
            name='transport_emission_factor_import_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='centerresource',
            name='use_emission_factor_import_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
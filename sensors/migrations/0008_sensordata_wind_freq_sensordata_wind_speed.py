# Generated by Django 5.2 on 2025-05-30 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sensors", "0007_sensordata_battery_voltage"),
    ]

    operations = [
        migrations.AddField(
            model_name="sensordata",
            name="wind_freq",
            field=models.FloatField(
                blank=True, help_text="Frekvens fra vindmåler (Hz)", null=True
            ),
        ),
        migrations.AddField(
            model_name="sensordata",
            name="wind_speed",
            field=models.FloatField(
                blank=True,
                help_text="Vindhastighet beregnet fra frekvens (m/s)",
                null=True,
            ),
        ),
    ]

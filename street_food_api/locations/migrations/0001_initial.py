# Generated by Django 3.1.5 on 2021-01-22 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("trucks", "0003_auto_20210121_1053"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "street",
                    models.CharField(max_length=100, verbose_name="Street"),
                ),
                (
                    "city",
                    models.CharField(max_length=100, verbose_name="City"),
                ),
                (
                    "zip_code",
                    models.CharField(max_length=7, verbose_name="Zip Code"),
                ),
                ("longitude", models.FloatField(verbose_name="Longitude")),
                ("latitude", models.FloatField(verbose_name="Latitude")),
                ("open_from", models.TimeField(verbose_name="Open from")),
                ("closed_at", models.TimeField(verbose_name="Closed at")),
                (
                    "truck",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="trucks.truck",
                        verbose_name="Truck",
                    ),
                ),
            ],
        ),
    ]
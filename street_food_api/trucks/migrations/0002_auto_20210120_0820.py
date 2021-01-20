# Generated by Django 3.1.5 on 2021-01-20 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trucks", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="paymentmethod",
            options={
                "verbose_name": "Payment Method",
                "verbose_name_plural": "Payment Methods",
            },
        ),
        migrations.AddField(
            model_name="truck",
            name="is_confirmed",
            field=models.BooleanField(default=False, verbose_name="Confirmed"),
        ),
    ]

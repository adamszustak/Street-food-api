from django.db import models
from django.utils.translation import ugettext_lazy as _
from trucks.models import Truck


class Location(models.Model):
    truck = models.OneToOneField(
        Truck, on_delete=models.CASCADE, verbose_name=_("Truck")
    )
    street = models.CharField(_("Street"), max_length=100)
    city = models.CharField(_("City"), max_length=100)
    zip_code = models.CharField(_("Zip Code"), max_length=7)
    longitude = models.FloatField(_("Longitude"))
    latitude = models.FloatField(_("Latitude"))
    latitude = models.FloatField(_("Latitude"))
    open_from = models.TimeField(_("Open from"))
    closed_at = models.TimeField(_("Closed at"))

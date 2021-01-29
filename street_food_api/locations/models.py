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
    longitude = models.FloatField(_("Longitude"), blank=True, null=True)
    latitude = models.FloatField(_("Latitude"), blank=True, null=True)
    open_from = models.TimeField(_("Open from"), blank=True, null=True)
    closed_at = models.TimeField(_("Closed at"), blank=True, null=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.truck.name

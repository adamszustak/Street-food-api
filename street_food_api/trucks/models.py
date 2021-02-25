import itertools

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from conf.utils import image_directory_path

from .managers import ConfirmedTruckManager


class Truck(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Owner"),
        on_delete=models.CASCADE,
        related_name="trucks",
    )
    name = models.CharField(_("Name"), max_length=50)
    phone = PhoneNumberField(_("Phone"), blank=True, max_length=50)
    email = models.EmailField(_("Email"), blank=True, max_length=50)
    city = models.CharField(_("City"), max_length=70)
    facebook = models.CharField(_("Facebook"), blank=True, max_length=50)
    instagram = models.CharField(_("Instagram"), blank=True, max_length=50)
    page_url = models.URLField(_("Page URL"), blank=True, max_length=200)
    description = models.CharField(_("Description"), max_length=200)
    payment_methods = models.ManyToManyField(
        "trucks.PaymentMethod", verbose_name=_("Payment Methods")
    )
    is_confirmed = models.BooleanField(_("Confirmed"), default=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    slug = models.SlugField(editable=False)

    objects = models.Manager()
    confirmed = ConfirmedTruckManager()

    class Meta:
        verbose_name = _("Truck")
        verbose_name_plural = _("Trucks")

    def __str__(self):
        return self.name

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not self.__class__.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = f"{slug_original}-{i}"
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)


class PaymentMethod(models.Model):
    payment_name = models.CharField(_("Payment Name"), max_length=30)

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")

    def __str__(self):
        return self.payment_name


class TruckImage(models.Model):
    truck = models.ForeignKey(
        "trucks.Truck",
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        verbose_name=_("Truck"),
    )
    image = models.ImageField(_("Image"), upload_to=image_directory_path)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f"{self.truck.name} - {self.image.name}"

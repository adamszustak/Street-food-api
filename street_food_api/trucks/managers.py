from django.db import models


class ConfirmedTruckManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=True)

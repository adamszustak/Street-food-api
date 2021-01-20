from django.db import models


class ConfirmedTruckQuerySet(models.QuerySet):
    def confirmed(self):
        return self.filter(is_confirmed=True)

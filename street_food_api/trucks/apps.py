from django.apps import AppConfig


class TrucksConfig(AppConfig):
    name = "trucks"

    def ready(self):
        import trucks.signals

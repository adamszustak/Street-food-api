import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.local")

app = Celery("street_food_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# poetry run celery -A conf worker --loglevel=INFO

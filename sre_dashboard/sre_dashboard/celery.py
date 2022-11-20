import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sre_dashboard.settings")
app = Celery("sre_dashboard")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
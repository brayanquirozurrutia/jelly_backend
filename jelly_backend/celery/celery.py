from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jelly_backend.settings')

app = Celery('jelly_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    worker_concurrency=2,
    worker_prefetch_multiplier=1,
    task_soft_time_limit=300,
)

app.autodiscover_tasks()

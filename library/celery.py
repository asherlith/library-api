import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
app = Celery('library')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

# using celery beat to schedule a task every week.
app.conf.beat_schedule = {
    # any name can be chosen
    'change-the-reader': {
        # where the task is located
        'task': 'book.tasks.reset_quantity',
        # when it will execute
        "schedule": timedelta(days=7),
        # arguments passed into the task function
        'args': (20,)
    }
}
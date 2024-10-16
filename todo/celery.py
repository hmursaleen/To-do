from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = Celery('todo')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in your Django apps automatically
app.autodiscover_tasks()

# Celery Beat for periodic tasks
app.conf.beat_schedule = {
    'check_deadline_tasks': {
        'task': 'tasks.tasks.check_upcoming_deadlines',
        'schedule': 3600.0,  # Run every hour
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

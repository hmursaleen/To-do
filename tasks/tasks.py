from celery import shared_task
from django.utils import timezone
from .models import Task

'''
@shared_task
def check_deadlines():
    """
    Task to check for approaching task deadlines and notify users.
    """
    now = timezone.now()
    tasks = Task.objects.filter(due_date__lte=now + timezone.timedelta(hours=24), is_completed=False)
    
    for task in tasks:
        # Notify the user, e.g., by sending an email or in-app notification.
        print(f"Notifying user {task.owner.email} about the approaching deadline for task: {task.title}")
'''





from time import sleep

@shared_task
def test_task():
    sleep(5)
    return 'Task completed'

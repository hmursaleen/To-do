# tasks/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from django.core.mail import send_mail
from django.contrib.auth.models import User

@shared_task
def check_upcoming_deadlines():
    # Define what is considered "upcoming" (e.g., tasks due in the next 24 hours)
    upcoming_time = timezone.now() + timedelta(hours=24)
    
    # Get tasks with a due date within the next 24 hours and are not completed
    upcoming_tasks = Task.objects.filter(due_date__lte=upcoming_time, is_completed=False)

    for task in upcoming_tasks:
        # Notify the owner of the task via email
        send_mail(
            'Task Deadline Approaching',
            f'The deadline for your task "{task.title}" is approaching.',
            'habibulmursaleen@gmail.com',  # Replace with your sender email
            [task.owner.email],
            fail_silently=False,
        )

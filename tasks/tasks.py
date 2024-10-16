import logging
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from tasks.models import Task
from celery import shared_task



logger = logging.getLogger(__name__)

@shared_task
def check_upcoming_deadlines():
    now = timezone.now()
    upcoming_deadline = now + timedelta(hours=24)

    tasks_due_soon = Task.objects.filter(due_date__range=(now, upcoming_deadline), is_completed=False)
    
    logger.info(f"Checking deadlines for {tasks_due_soon.count()} tasks")

    for task in tasks_due_soon:
        try:
            send_mail(
                subject=f"Task Deadline Approaching: {task.title}",
                message=f"Your task '{task.title}' is due on {task.due_date}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[task.owner.email],
            )
            logger.info(f"Email sent to {task.owner.email} for task {task.title}")
        except Exception as e:
            logger.error(f"Failed to send email to {task.owner.email}: {e}")

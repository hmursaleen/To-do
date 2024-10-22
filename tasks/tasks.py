import logging
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from tasks.models import Task
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

@shared_task
def check_upcoming_deadlines():
    now = timezone.now()
    upcoming_deadline = now + timedelta(hours=24)

    tasks_due_soon = Task.objects.filter(due_date__range=(now, upcoming_deadline), is_completed=False)
    
    logger.info(f"Checking deadlines for {tasks_due_soon.count()} tasks")

    channel_layer = get_channel_layer()

    for task in tasks_due_soon:
        try:
            # Send email notification
            send_mail(
                subject=f"Task Deadline Approaching: {task.title}",
                message=f"Your task '{task.title}' is due on {task.due_date}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[task.owner.email],
            )
            logger.info(f"Email sent to {task.owner.email} for task {task.title}")

            # Send WebSocket notification
            notification_message = f"Task '{task.title}' is approaching its deadline on {task.due_date}."
            
            logger.info(f"WebSocket notification prepared for user {task.owner.id} for task {task.title}")
            async_to_sync(channel_layer.group_send)(
                f"user_{task.owner.id}_notifications",  # Send to the user group
                {
                    'type': 'send_deadline_notification',
                    'notification': notification_message
                }
            )
            logger.info(f"WebSocket notification dispatched to group user_{task.owner.id}_notifications")

        except Exception as e:
            logger.error(f"Failed to send notification to {task.owner.email}: {e}")

'''
post_save Signal: The post_save signal is triggered whenever a new Membership instance is saved. In this case, we check if the Membership is created and if the role is MEMBER (indicating a user is added as a regular member to a team).
Notification Creation: A notification is created and saved in the database for the user who is added to the team.
Real-Time Notification: A placeholder call to send_realtime_notification is used to send a real-time notification to the user via Django Channels (we'll implement this part shortly).
'''


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Membership
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Membership)
def notify_user_on_addition(sender, instance, created, **kwargs):
    """
    Signal handler to notify a user when they are added to a team.
    """
    # Only send a notification when a new Membership is created
    if created and instance.role == Membership.MEMBER:
        # Get the user and team details
        user = instance.user
        team = instance.team
        admin_user = instance.team.memberships.filter(role=Membership.ADMIN).first().user

        # Create a notification message
        message = f"You have been added to the team '{team.name}' by {admin_user.username}."

        # Save the notification in the database
        Notification.objects.create(
            user=user,
            message=message
        )

        # Broadcast the real-time notification via Django Channels (Step 3 will cover this)
        # Assuming a function called send_realtime_notification is defined elsewhere
        from notification.utils import send_realtime_notification
        send_realtime_notification(user.id, message)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


'''
Channel Layer: This function retrieves the channel layer using get_channel_layer().
User Group: Each user is part of a unique group (e.g., user_1 for user_id=1), allowing us to target specific users for notifications.
Broadcast: The function uses group_send to broadcast a message to the targeted user's group.
'''



def send_realtime_notification(user_id, message):
    """
    Utility function to send a real-time notification to the user.
    """
    channel_layer = get_channel_layer()
    # The group name for the specific user to receive the notification
    group_name = f'user_{user_id}'

    # Sending the message to the user's channel group
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'message': message,
        }
    )

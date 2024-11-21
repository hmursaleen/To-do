import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now

class DeadlineNotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_{self.scope['user'].id}_notifications"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            # Log successful WebSocket connection
            print(f"WebSocket connection established for user {self.scope['user'].id} in group {self.group_name}")


    async def disconnect(self, close_code):
        # Logic to leave the group when the WebSocket disconnects.
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Optional: Handle incoming messages from the WebSocket if needed.
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Echo the received message back to the WebSocket (optional)
        await self.send(text_data=json.dumps({'message': message}))


    async def send_deadline_notification(self, event):
        notification = event['notification']
        
        # Debugging log
        print(f"Sending WebSocket notification: {notification}")
        
        await self.send(text_data=json.dumps({
            'notification': notification,
            'timestamp': now().isoformat()
        }))








'''
connect Method: Handles WebSocket connection and adds the user to a unique group based on their user ID.
disconnect Method: Handles disconnection and removes the user from the group.
send_notification Method: Receives notification data from the Redis channel and sends it to the WebSocket.
'''


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the user ID from the scope (assuming authentication is in place)
        self.user_id = self.scope['user'].id

        # Generate a unique group name based on the user's ID
        self.group_name = f'user_{self.user_id}'

        # Join the user's notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the user's notification group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        # Receive notification message from the channel layer
        message = event['message']

        # Send the notification message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

'''
User-Specific Channel: The group name is based on the user_id, allowing targeted notifications.
Real-Time Notifications: The send_notification method sends the received message to the user's WebSocket.
'''
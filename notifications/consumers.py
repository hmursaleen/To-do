import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now

class DeadlineNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Logic to handle new WebSocket connection.
        self.group_name = f"user_{self.scope['user'].id}_notifications"
        
        # Join the group for this user to receive notifications.
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Logic to leave the group when the WebSocket disconnects.
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # This will handle receiving a message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Echo the received message back to the WebSocket (optional)
        await self.send(text_data=json.dumps({'message': message}))

    async def send_deadline_notification(self, event):
        # Method to send deadline notifications to the WebSocket
        notification = event['notification']
        
        # Send the notification to the WebSocket client
        await self.send(text_data=json.dumps({
            'notification': notification,
            'timestamp': now().isoformat()
        }))


'''
connect(self):

When a WebSocket connection is established, the consumer connects the user to a group based on their user ID (e.g., user_1_notifications). This will allow the consumer to send notifications to specific users.
disconnect(self, close_code):

When the WebSocket connection is closed, the user is removed from the group.
receive(self, text_data):

This method handles incoming messages from the WebSocket client (though for notifications, we won't typically need this unless the client sends specific requests).
send_deadline_notification(self, event):

This method sends notifications to the user when the event is triggered (i.e., when a task is approaching a deadline).
'''
from django.urls import path
from .consumers import DeadlineNotificationConsumer

websocket_urlpatterns = [
    path('ws/notifications/deadlines/', DeadlineNotificationConsumer.as_asgi()),  # Deadline notifications
    # Future routes for other types of notifications, like task sharing, can be added here.
    # path('ws/notifications/task-sharing/', TaskSharingNotificationConsumer.as_asgi()),
    # path('ws/notifications/status-update/', StatusUpdateNotificationConsumer.as_asgi()),
]


'''
This defines the WebSocket route, /ws/notifications/, that connects to the DeadlineNotificationConsumer. When a client opens a WebSocket connection at this URL, the DeadlineNotificationConsumer will be invoked.
'''
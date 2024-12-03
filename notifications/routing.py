from django.urls import path
from .consumers import DeadlineNotificationConsumer, NotificationConsumer

websocket_urlpatterns = [
    path('ws/notifications/deadlines/', DeadlineNotificationConsumer.as_asgi()),  # Deadline notifications
    path('ws/notifications/team-invite/', NotificationConsumer.as_asgi()),
    # path('ws/notifications/task-sharing/', TaskSharingNotificationConsumer.as_asgi()),
    # path('ws/notifications/status-update/', StatusUpdateNotificationConsumer.as_asgi()),
]

'''
from django.urls import re_path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
'''



'''
This defines the WebSocket route, /ws/notifications/team-invite/, that connects to the DeadlineNotificationConsumer. When a client opens a WebSocket connection at this URL, the DeadlineNotificationConsumer will be invoked.
'''
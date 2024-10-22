# todo/asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import notifications.routing  # Import WebSocket routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests
    "websocket": AuthMiddlewareStack(  # Handle WebSocket requests
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})

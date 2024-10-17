from django.core.asgi import get_asgi_application  # Import the ASGI application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notifications.routing  # Use your app-level routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns  # App-level WebSocket routing
        )
    ),
})


'''
ProtocolTypeRouter: This router allows Django Channels to distinguish between HTTP and WebSocket protocols.
AuthMiddlewareStack: Wraps the WebSocket connection with Django authentication, so the consumer can access self.scope['user'] to identify the user.
'''
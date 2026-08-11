import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import breakerapi.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breadbreaker.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            breakerapi.routing.websocket_urlpatterns,
        )
    ),
})
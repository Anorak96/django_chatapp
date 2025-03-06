import os
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns 
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatAPI.settings')

http_response_app = get_asgi_application()

application =ProtocolTypeRouter({
    "http": http_response_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    )
})

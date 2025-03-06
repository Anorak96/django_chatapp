import os
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns 
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatAPI.settings')

http_response_app = get_asgi_application()

application =ProtocolTypeRouter({
    "http": http_response_app,
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})

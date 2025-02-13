"""
ASGI config for ABSCS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from tcp_client.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ABSCS.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Standard Django HTTP
    "websocket": URLRouter(websocket_urlpatterns),  # WebSockets
})
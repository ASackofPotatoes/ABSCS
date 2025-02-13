from django.urls import path
from .consumers import TelemetryConsumer, ConnectionConsumer

websocket_urlpatterns = [
    path("ws/telemetry/", TelemetryConsumer.as_asgi()),
    path("ws/connection/", ConnectionConsumer.as_asgi())
]
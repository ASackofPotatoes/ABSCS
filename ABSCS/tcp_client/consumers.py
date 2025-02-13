from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("telemetry_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("telemetry_group", self.channel_name)

    async def receive(self, text_data):
        # Handle messages from the frontend if needed
        pass

    async def send_telemetry(self, event):
        """Broadcasts telemetry data to all connected clients"""
        data = event["data"]
        await self.send(text_data=json.dumps(data))

class ConnectionConsumer(AsyncWebsocketConsumer):
    pass
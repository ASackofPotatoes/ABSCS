from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
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
    async def connect(self):
        await self.accept()
        if cache.get("mission_name") and cache.get("profile_name"):
            #Send current connection status, which is set by tcp handler on success
            await self.send(text_data=json.dumps({"status": "connection_success",
                                                "mission_name" : cache.get("mission_name"),
                                                "profile_name" : cache.get("profile_name")}))
        
        await self.channel_layer.group_add("connection_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("connection_group", self.channel_name)

    async def receive(self, text_data):
        pass

    from django.core.cache import cache

    async def connection_success(self, event):
        mission_name = event["mission_name"]
        profile_name = event["profile_name"]
        
        cache.set("mission_name", mission_name, timeout=None)
        cache.set("profile_name", profile_name, timeout=None)

        await self.send(text_data=json.dumps({
            "status": "connection_success",
            "mission_name": mission_name,
            "profile_name": profile_name
        }))

    
    async def connection_lost(self, event):
        message = event["message"]
        cache.set("current_mission", None, timeout=None)
        cache.set("current_profile", None, timeout=None)

        await self.send(text_data=json.dumps({
            "status": "connection_lost",
            "message": message
        }))


        

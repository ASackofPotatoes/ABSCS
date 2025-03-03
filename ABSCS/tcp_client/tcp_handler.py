import asyncio
import socket

from channels.layers import get_channel_layer
from django.core.cache import cache

async def tcp_client(ip, port, mission_name:str=None, profile_name:str=None):
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        channel_layer = get_channel_layer()



        # Added mission and profile name to this so that the success message is self-contained.
        await channel_layer.group_send(
            "connection_group",
            {"type": "connection_success", "message": "Connected to TCP server.", "mission_name": mission_name, "profile_name" : profile_name}
        )

        try:
            while True:
                data = await reader.readline()

                if not data:
                    # Server closed connection gracefully
                    cache.set("current_mission", None, timeout=None)
                    cache.set("current_profile", None, timeout=None)

                    await channel_layer.group_send(
                        "connection_group",
                        {"type": "connection_lost", "message": "Connection closed by server."}
                    )
                    break

                # Send telemetry to WebSocket group
                await channel_layer.group_send(
                    "telemetry_group",
                    {"type": "send_telemetry", "data": data.decode("utf-8")}
                )

        except (asyncio.CancelledError, ConnectionResetError):
            await channel_layer.group_send(
                "connection_group",
                {"type": "connection_lost", "message": "Connection lost unexpectedly."}
            )

        except asyncio.TimeoutError:
            await channel_layer.group_send(
                "connection_group",
                {"type": "connection_lost", "message": "Network timeout, connection lost."}
            )

        finally:
            writer.close()
            await writer.wait_closed()

    except (OSError, asyncio.TimeoutError, ConnectionRefusedError) as e:
        channel_layer = get_channel_layer()
        # Handle cases where the connection fails to open
        await channel_layer.group_send(
            "connection_group",
            {"type": "connection_lost", "message": f"Failed to connect to data server", "errorMessage" : f"{str(e)}"}
        )


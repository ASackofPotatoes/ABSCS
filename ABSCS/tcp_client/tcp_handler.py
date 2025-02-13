import asyncio
import socket

from channels.layers import get_channel_layer

async def tcp_client(ip, port):
    reader, writer = await asyncio.open_connection(ip, port)
    
    channel_layer = get_channel_layer()

    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            #FIGURE OUT HOW TO GROUP JSONS TOGETHER BEFORE SENDING
            # Send data to WebSocket group

            await channel_layer.group_send(
                "telemetry_group",
                {"type": "send_telemetry", "data": data.decode("utf-8")}
            )

    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()




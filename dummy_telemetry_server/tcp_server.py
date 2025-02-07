import asyncio
import json
import random
from datetime import datetime, timezone

HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 12345      # Port to accept connections

MNEMONICS = ["BATT_VOLTAGE", "BATT_TEMP", "SPIN_X", "SPIN_Y", "SPIN_Z"]

def generate_telemetry():
    """Generates random telemetry data in the expected format."""
    telemetry_data = {
        "source": "Ex-Alta 3",
        "ground_station": "ECERF",
        "telemetry": [],
        "format_version": "1.0"
    }

    for mnemonic in MNEMONICS:
        telemetry_data["telemetry"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
            "mnemonic": mnemonic,
            "type": "float",
            "data": round(random.uniform(-100, 100), 5)  # Random float between -100 and 100
        })

    return json.dumps(telemetry_data) + "\n"  # Add newline for easy parsing

async def handle_client(reader, writer):
    """Handles a client connection."""
    addr = writer.get_extra_info('peername')
    print(f"Client connected: {addr}")

    try:
        while True:
            telemetry_json = generate_telemetry()
            writer.write(telemetry_json.encode())
            await writer.drain()
            print(f"Sent: {telemetry_json.strip()}")  # Log sent data
            await asyncio.sleep(1)  # Send telemetry every second

    except asyncio.CancelledError:
        print(f"Client {addr} disconnected.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    """Starts the TCP server."""
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"TCP Server running on {addr}")

    async with server:
        await server.serve_forever()

# Run the server
asyncio.run(main())


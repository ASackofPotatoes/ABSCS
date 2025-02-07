import asyncio

HOST = "127.0.0.1"  # Change this to the server's IP if needed
PORT = 12345        # Must match the server port

async def tcp_client():
    """Connects to the TCP server and continuously prints received telemetry data."""
    while True:
        try:
            print(f"Connecting to {HOST}:{PORT}...")
            reader, writer = await asyncio.open_connection(HOST, PORT)
            print("Connected! Waiting for telemetry data...\n")

            while True:
                data = await reader.readline()  # Read a full JSON message (newline-terminated)
                if not data:
                    print("Connection closed by server.")
                    break

                print(f"Received: {data.decode().strip()}")

        except (ConnectionRefusedError, asyncio.TimeoutError):
            print("Connection failed. Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

asyncio.run(tcp_client())

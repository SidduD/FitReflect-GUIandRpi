import asyncio
import websockets
import json

async def receive_data():
    # Define the WebSocket server URL
    websocket_server_url = "ws://localhost:8765"

    async with websockets.connect(websocket_server_url) as websocket:
        print("Connected to WebSocket server.")
        while True:
            try:
                data = await websocket.recv()
                parsed_data = json.loads(data)
                print("Received data:", parsed_data)
            except websockets.exceptions.ConnectionClosed:
                print("Connection to server closed.")
                break

# Run the asyncio event loop
asyncio.run(receive_data())

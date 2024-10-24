import websockets
import asyncio
import json

# Server data
PORT = 8765
print("Server listening on Port " + str(PORT))

# A set of connected ws clients
connected = set()

# The main behavior function for this server
async def echo(websocket, path):
    print("A client just connected")
    # Store a copy of the connected client
    connected.add(websocket)
    await websocket.send(json.dumps({"message" : "Welcome"}))
    # Handle incoming messages
    try:
        async for message in websocket:
            print('Received message from client: : {}'.format(message))
            # Send a response to all connected clients except sender
            for conn in connected:
                if conn != websocket:
                    res = json.loads(message)
                    await conn.send(json.dumps(res))
    # Handle disconnecting clients 
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        connected.remove(websocket)

# Start the server
start_server = websockets.serve(echo, "0.0.0.0", PORT, max_queue=2**5)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
import asyncio
import websockets

# Store connected clients
clients = set()


async def signal_handler(websocket, path):
    try:
        # Add the new client to the set of connected clients
        clients.add(websocket)

        async for message in websocket:
            # Broadcast the message to all connected clients (broadcast signaling)
            await asyncio.gather(
                *[client.send(message) for client in clients if client != websocket]
            )

    except websockets.ConnectionClosed:
        pass
    finally:
        # Remove the client from the set when they disconnect
        clients.remove(websocket)

if __name__ == "__main__":
    server = websockets.serve(signal_handler, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

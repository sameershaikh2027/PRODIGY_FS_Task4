import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket):
    # Add client to the set of connected clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the message to other connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.ConnectionClosed:
        pass
    finally:
        # Remove the client from the set
        connected_clients.remove(websocket)

async def main():
    # Start WebSocket server
    async with websockets.serve(handle_client, "0.0.0.0", 6789):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import websockets
import uuid
import json
import websocket
from doorsProject.emaiManager import *
from doorsProject.payloadCollection import PayloadCollection


class WebSocketServer:
    connected_clients = {}
    all_instances = []

    def __init__(self):
        self.connected_clients = {}
        self.all_instances.append(self)

    async def handle_client(self, websocket, path):
        client_id = str(uuid.uuid4())  # Generate a unique ID for the client
        self.connected_clients[client_id] = websocket

        client_ip = websocket.remote_address
        print(f"New client connected: {websocket.remote_address}")
        try:
            sendGmail_ramziVersion(
                f"{client_ip} is connected",
                subject="hallo from backupWsServer",
            )
        except Exception as e:
            print(e)
            pass

        try:
            while True:
                message_str = await websocket.recv()
                message = json.loads(message_str)
                print(f"Received message from client {client_id}: {message}")
                await self.broadcast(
                    message, sender_id=client_id
                )  # Broadcast message to all clients
        except websockets.ConnectionClosed:
            del self.connected_clients[client_id]
            # Remove the client when disconnected
            disconnect_message = {
                "message from Local WS Server": f"Client {client_ip} has disconnected.",
            }
            try:
                sendGmail_ramziVersion(
                    f"{client_ip} has disconnected.",
                    subject="hallo from backupWsServer",
                )
            except Exception as e:
                print(e)
                pass
            print(disconnect_message)
            await self.broadcast(
                disconnect_message,
            )
        except websockets.ConnectionClosedOK:
            print("closed is ok")

        except websocket.WebSocketConnectionClosedException:
            print("WebSocket connection closed.")
        except (websockets.ConnectionClosed, websockets.ConnectionClosedError):
            del self.connected_clients[
                client_id
            ]  # Remove the client's WebSocket from the dictionary
            disconnect_message = {
                "message from Local WS Server": f"Client {client_id} has disconnected.",
            }
            print(disconnect_message)
            await self.broadcast(
                disconnect_message,
            )

        finally:
            # Make sure to close the connection properly
            await websocket.close()

    async def broadcast(self, message, sender_id=None):
        # Convert the Python object to a JSON string
        message_str = json.dumps(message)
        # Send the message to all connected clients

        for client_id, client_websocket in self.connected_clients.items():
            try:
                for client in self.connected_clients:
                    if sender_id != client:
                        await client_websocket.send(message_str)
            except websockets.ConnectionClosedError as e:
                print(f"Error sending message: {e}")

    # async def manual_broadcast(self, message):
    # Function to manually broadcast a message to all connected clients
    # await self.broadcast(message)


async def start_server():
    ws = WebSocketServer()
    server = await asyncio.start_server(
        ws.handle_client,
        PayloadCollection.localWsServerIp,
        PayloadCollection.localWsServerPort,
    )

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()


# Run the server using asyncio.run()
asyncio.run(start_server())

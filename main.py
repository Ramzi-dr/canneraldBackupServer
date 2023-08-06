import asyncio
import websockets
import uuid
import json
from doorsProject.emaiManager import *
from doorsProject.payloadCollection import PayloadCollection

from doorsProject.glutzMain import *


class WebSocketServer:
    def __init__(self):
        self.all_instances = []
        self.connected_clients = {}
        self.all_instances.append(self)

    async def handle_client(self, websocket, path):
        client_id = str(uuid.uuid4())  # Generate a unique ID for the client
        self.connected_clients[client_id] = websocket
        take_overToggle(False)
        client_ip = websocket.remote_address
        print(f"the event server:{client_ip}  is online and doing well")
        # try:
        #     sendGmail_ramziVersion(
        #         f"the event server with ip: {client_ip} is connected",
        #         subject="hallo from backupWsServer event.",
        #     )
        # except Exception as e:
        #     print(e)
        #     pass

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
            take_overToggle(True)
            await run_GlutzListener()

            # try:
            #     sendGmail_ramziVersion(
            #         f"the event server with ip: {client_ip} has disconnected.",
            #         subject="hallo from backupWsServer",
            #     )
            # except Exception as e:
            #     print(e)
            #     pass
            # await self.broadcast( # need this only if u want to send message to other connected clients
            #     disconnect_message,
            # )
        except websockets.ConnectionClosedOK:
            print("closed is ok")

        except websocket.WebSocketConnectionClosedException:
            print("WebSocket connection closed.")
        except (websockets.ConnectionClosed, websockets.ConnectionClosedError):
            take_overToggle(True)
            await run_GlutzListener()

            # try:
            #     sendGmail_ramziVersion(
            #         f"the event server with ip: {client_ip} has disconnected.",
            #         subject="hallo from backupWsServer",
            #     )
            # except Exception as e:
            #     print(e)
            #     pass
            del self.connected_clients[
                client_id
            ]  # Remove the client's WebSocket from the dictionary
            # disconnect_message = {
            #     "message from Local WS Server": f"Client {client_id} has disconnected.",
            # }
            # await self.broadcast(
            #     disconnect_message,
            # )

        finally:
            # Make sure to close the connection properly
            await websocket.close()

    ###########################################  broadcast function need if more clients #############################
    # async def broadcast(self, message, sender_id=None):
    #     # Convert the Python object to a JSON string
    #     message_str = json.dumps(message)
    #     # Send the message to all connected clients

    # for client_id, client_websocket in self.connected_clients.items():
    #     try:
    #         for client in self.connected_clients:
    #             if sender_id != client:
    #                 await client_websocket.send(message_str)
    #     except websockets.ConnectionClosedError as e:
    #         print(f"Error sending message: {e}")
    ##################################################################################################################
    async def start_server(self):
        server = await websockets.serve(
            self.handle_client,
            "localhost",
            PayloadCollection.localWsServerPort,
            ping_timeout=None,
        )
        print("Server running...")
        await asyncio.sleep(3)  # Wait for 10 seconds before checking connected clients
        if not self.connected_clients:
            print(
                "I've been running for more than 30 seconds and the event"
                "server hasn't connected so far.\n and i'm taking over, "
            )
            take_over = True
            await run_GlutzListener()
            # try:
            #     sendGmail_ramziVersion(
            #         "I've been running for more than 30 seconds and"
            # "the event server hasn't connected so far.",
            #         subject="hallo from backupWsServer, the event server did not show up",
            #     )
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            pass

        await server.wait_closed()


if __name__ == "__main__":
    try:
        server = WebSocketServer()
        asyncio.get_event_loop().run_until_complete(server.start_server())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
        # try:
        #     sendGmail_ramziVersion(
        #         f"there is Error occured and got Exception while starting the backup Ws Server:  \n {e}",
        #         subject="hallo from backupWsServer,Error while starting",
        #     )
        # except Exception as e:
        #     print(e)
        #     pass

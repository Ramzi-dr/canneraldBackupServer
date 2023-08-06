import asyncio
import json
import websockets
from virtualGlutzUserAction import VirtualUserAction
from doorsProject.payloadCollection import PayloadCollection

uri = PayloadCollection.localWsServerUrl
keep_connection = True
message_to_send = ""


async def connect_and_send():
    global keep_connection
    global message_to_send

    try:
        async with websockets.connect(uri) as ws:
            while keep_connection:
                message = input(
                    "Enter message to send (code, badge, master code, master badge or master long): "
                )
                message_to_send = ""

                if message == "code":
                    message_to_send = VirtualUserAction.bs4UserCode
                elif message == "badge":
                    message_to_send = VirtualUserAction.bst4UserBadge
                elif message == "code1":
                    message_to_send = VirtualUserAction.bs1UserCode
                elif message == "badge1":
                    message_to_send = VirtualUserAction.bs1UserBadge
                elif message == "master code":
                    message_to_send = VirtualUserAction.masterCode
                elif message == "master badge":
                    message_to_send = VirtualUserAction.masterBadge
                elif message == "master long":
                    message_to_send = VirtualUserAction.masterBadgeLong
                elif message == 'rise':
                    message_to_send = VirtualUserAction.risingEdge
                elif message == 'fall':
                    message_to_send = VirtualUserAction.fallingEdge
                elif message == 'state 0':
                    message_to_send = VirtualUserAction.stateInput_0
                elif message == 'state 1':
                    message_to_send = VirtualUserAction.stateInput_1
                elif message == "exit":
                    keep_connection = False
                    break

                await ws.send(json.dumps(message_to_send))

                # Receive and print the response message
                response = await ws.recv()
                print(f"Received message: {response}")

    except KeyboardInterrupt:
        print("close")
        keep_connection = False
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed.")
        keep_connection = False


asyncio.get_event_loop().run_until_complete(asyncio.gather(connect_and_send()))

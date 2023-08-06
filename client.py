import asyncio
import json
import websockets
from virtualGlutzUserAction import VirtualUserAction
from doorsProject.payloadCollection import PayloadCollection

uri = PayloadCollection.localWsServerUrl

message_to_send = ""


async def connect_and_send():
    global message_to_send
    counter = 0

    while counter < 500000:

        try:
            async with websockets.connect(uri) as ws:
                while True:
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
        except ConnectionRefusedError:
            print(
                f"Hoi We don't have a connection. Please control the {serverInfo} Server."
            )
            await asyncio.sleep(1)
            print(f"I am trying to reconnect for the {counter} time.")
            counter += 1

            if counter == 5 or counter == 50 or counter == 150:
                # sendGmail(
                #     f"{serverInfo} is down. Please control the connection.",
                #     subject=f"Can't connect to {serverInfo}",
                # )
                print(counter)

        except (
            websockets.exceptions.ConnectionClosedOK,
            websockets.exceptions.ConnectionClosedError,
        ):
            print(f"Hoi We lost connection. Please control the Internet. {serverInfo}")
            await asyncio.sleep(1)
            print(f"I am trying to reconnect for the {counter} time.")
            counter += 1

            # if counter == 5 or counter == 50 or counter == 150:
            #     sendGmail(
            #         f"{serverInfo} is down. Please control the connection.",
            #         subject=f"Can't connect to {serverInfo}",
            #     )

        except OSError:
            await asyncio.sleep(1)

            print(
                f"Server: serverInfo is down. There is no connection, and I will try to reconnect for the {counter} time."
            )
            counter += 1
            # if counter == 5 or counter == 50 or counter == 150:
            #     sendGmail(
            #         f"{serverInfo} is down. Please control the connection.",
            #         subject=f"Can't connect to {serverInfo}",
            #     )

        except asyncio.exceptions.TimeoutError:
            await asyncio.sleep(1)
            counter += 1
        except websockets.ConnectionClosed:
            continue

async def start_thread():
    await connect_and_send()


asyncio.get_event_loop().run_until_complete(start_thread())

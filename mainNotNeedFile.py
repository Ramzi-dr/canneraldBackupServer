import asyncio
import websockets.exceptions
from websockets import connect
from doorsProject.payloadCollection import PayloadCollection
from doorsProject.observer import *
from doorsProject.payloadCollection import *
from doorsProject.emaiManager import sendGmail
import threading
from doorsProject.accessManager import AccessManager
from doorsProject.messageFilter import MessageFilter
from doorsProject.glutzMain import run_GlutzListener
from doorsProject.glutzMain import should_stop_listeners


async def take_over(counter):
    if counter == 5:
        await run_GlutzListener()


async def listen(url, serverInfo):
    counter = 0
    global should_stop_listeners
    connected = False

    while True:
        try:
            async with connect(url) as websocket:
                await websocket.send(json.dumps("hoi from the Backup Server"))
                print("Hoi from the Backup Server I'm Connected to the event Server")

                while True:
                    message = json.loads(await websocket.recv())
                    print(message)
                    connected = True
                    counter = 0

                    # ... Continue processing existing door_ids ...

        except ConnectionRefusedError:
            print(
                f"Hoi We don't have a connection. (ConnectionRefusedError) Please control the {serverInfo} Server."
            )
            await asyncio.sleep(1)
            print(f"I am trying to reconnect for the {counter} time.")
            counter += 1

            if counter == 5:
                counter += 1
                await take_over(counter=counter)
                # sendGmail(
                #     f"{serverInfo} is down.(ConnectionRefusedError) Please control the connection.",
                #     subject=f"Can't connect to {serverInfo}",
                # )

        except (
            websockets.exceptions.ConnectionClosedOK,
            websockets.exceptions.ConnectionClosedError,
        ):
            print(f"Hoi We lost connection. Please control the Internet. {serverInfo}")
            await asyncio.sleep(1)
            print(f"I am trying to reconnect for the {counter} time.")
            counter += 1

            await take_over(counter=counter)
            # sendGmail(
            #     f"{serverInfo} is down. Please control the connection.",
            #     subject=f"Can't connect to {serverInfo}",
            # )

        except OSError:
            await asyncio.sleep(1)

            print(
                f"Server: {serverInfo} is down. There is no connection, and I will try to reconnect for the {counter} time."
            )
            counter += 1
            await take_over(counter=counter)

            # sendGmail(
            #     f"{serverInfo} is down. Please control the connection.",
            #     subject=f"Can't connect to {serverInfo}",
            # )

        except asyncio.exceptions.TimeoutError:
            await asyncio.sleep(1)
            counter += 1
            await take_over(counter=counter)
        except websockets.ConnectionClosed:
            continue
        connected = False


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            listen(
                url=PayloadCollection.eventWsServerUrl,
                serverInfo=PayloadCollection.eventWsServerIp,
            ),
        )
    )

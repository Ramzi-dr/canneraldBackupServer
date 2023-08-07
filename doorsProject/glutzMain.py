import asyncio
import websockets.exceptions
from websockets import connect
from doorsProject.observer import Observer
from doorsProject.payloadCollection import *
from doorsProject.emailManager import *
import threading
from doorsProject.accessManager import AccessManager
from doorsProject.messageFilter import MessageFilter

# Define the global variable 'doors_instances' at the module level
doors_instances = {}


def delete_door_instance(door_id):
    global doors_instances
    thread_id = threading.current_thread().ident
    if (thread_id, door_id) in doors_instances:
        del doors_instances[(thread_id, door_id)]
        print(f"Threading stopped for door instance. {door_id}")


def add_door_instance(door_id):
    global doors_instances
    thread_id = threading.current_thread().ident
    doors_instances[(thread_id, door_id)] = doors_instances.get(
        (thread_id, door_id), create_observer()
    )
    print("door is add instance")


def create_observer():
    access_manager = AccessManager(
        doors_instances, delete_door_instance
    )  # Pass the doors_instances and delete_door_instance function
    if access_manager is None:
        print("Access manager is None in create_observer()")
        return None
    return Observer(access_manager)


async def handle_door(door_id, data):
    add_door_instance(door_id=door_id)

    observer = doors_instances.get((threading.current_thread().ident, door_id))
    if observer is None:
        observer = create_observer()
        doors_instances[(threading.current_thread().ident, door_id)] = observer

    # The observer object might be None if `create_observer()` returns None.
    if observer:
        await observer.observer(data)
    else:
        print(f"Observer is None for door_id: {door_id}")


take_over = True


async def listen(url, serverInfo):
    counter = 0
    while take_over:
        print("im running till the main server is back")
        while counter < 500000 and take_over:
            try:
                async with connect(url) as websocket:
                    await websocket.send(json.dumps(PayloadCollection.message))
                    print(
                        "Hoi from the Backup Server I'm Connected to the  Glutz Server"
                    )
                    counter = 0

                    while take_over:
                        message = json.loads(await websocket.recv())
                        if take_over == True:
                            print(message)
                            message_filter = MessageFilter()
                            data = message_filter.messageFilter(message=message)
                            door = message_filter.get_door_id(message=message)

                            if door is not None:
                                if door not in doors_instances:
                                    # Start a new thread or process to handle the new door_id
                                    asyncio.create_task(handle_door(door, data))
                                else:
                                    observer = doors_instances.get(
                                        (threading.current_thread().ident, door)
                                    )
                                    await observer.observer(data)
                        # ... Continue processing existing door_ids ...
            except ConnectionRefusedError:
                print(
                    f"Hoi We don't have a connection. Please control the {serverInfo} Server."
                )
                await asyncio.sleep(1)
                print(f"I am trying to reconnect for the {counter} time.")
                counter += 1
                # if counter == 5 or counter == 50 or counter == 150:
                #     exceptionMessage = "ConnectionRefusedError"
                #     sendMail_afterException(
                #         serverInfo=serverInfo, exeption=exceptionMessage
                #     )

            except (
                websockets.exceptions.ConnectionClosedOK,
                websockets.exceptions.ConnectionClosedError,
            ):
                print(
                    f"Hoi We lost connection. Please control the Internet. {serverInfo}"
                )
                await asyncio.sleep(1)
                print(f"I am trying to reconnect for the {counter} time.")
                # if counter == 5 or counter == 50 or counter == 150:
                #     exceptionMessage = "websockets.exceptions.ConnectionClosedOK-ConnectionClosedError,"
                #     sendMail_afterException(
                #         serverInfo=serverInfo, exeption=exceptionMessage
                #     )

            except OSError:
                await asyncio.sleep(1)

                print(
                    f"Server: {serverInfo} is down. There is no connection, and I will try to reconnect for the {counter} time."
                )
                counter += 1
                if counter == 5 or counter == 50 or counter == 150:
                    exceptionMessage = ("OSError,",)

                    sendMail_afterException(
                        serverInfo=serverInfo, exeption=exceptionMessage
                    )

            except asyncio.exceptions.TimeoutError:
                await asyncio.sleep(1)
                counter += 1
                # if counter == 5 or counter == 50 or counter == 150:
                #     exceptionMessage = "asyncio.exceptions.TimeoutError,"
                #     sendMail_afterException(
                #         serverInfo=serverInfo, exeption=exceptionMessage
                #     )

            except websockets.ConnectionClosed:
                continue
            await asyncio.sleep(1)
    print("i stop running  the event server is online")


async def run_GlutzListener():
    asyncio.create_task(
        listen(
            url=PayloadCollection.canneraldWsServerUrl,
            serverInfo=PayloadCollection.GlutzUrl,
        )
    )


def take_overToggle(value):
    global take_over
    take_over = value


def sendMail_afterException(serverInfo, exeption):
    try:
        sendGmail_ramziVersion(
            f"Hoi We don't have a connection. Please control the {serverInfo} Server.\nError: {exeption}",
            subject="hallo from backupWsServer event.",
        )
    except Exception as e:
        print(e)
        pass

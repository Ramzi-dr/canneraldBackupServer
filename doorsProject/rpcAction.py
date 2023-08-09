from doorsProject.rpcCommands import *


class RpcAction:
    def __init__(self):
        self.doorIsOpen = None

    def activate_Reader_Output(self, readerId, outputNum=0):
        print("blink blink......" + "\N{winking face}")
        activateReader_Ouput(readerId=readerId, outputNum=outputNum)

    def activate_IO_Output(
        self,
        IO_Module,
        media,
        readerId,
        activationModus=None,
        outputNum=PayloadCollection.IO_ModuleRelay_1,
    ):
        user_label = get_userLabel(
            user_id=get_userIdByMedia_info(publicMediaLabel=media)
        )
        door_label = get_doorLabel(
            accessPointId=get_accessPointIdByReaderId_info(deviceId=readerId)
        )
        print(f"user: {user_label} have access to door: {door_label} 👍")

        if activationModus == "keep_it_open/close_it":
            openOrClose_door(deviceId=IO_Module, outputNum=outputNum)

        else:
            openDoor_short(deviceId=IO_Module, outputNum=outputNum)

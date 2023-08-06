from doorsProject.accessManager import AccessManager


class Observer:
    def __init__(
        self,
        access_manager,
    ):
        self.access_manager = access_manager

    async def observer(self, data):
        events = data["events"][0]
        if events["event"] == "RFID Media":
            badgeId = events["publicMediaLabel"]
            reader = data["deviceid"]
            isLong = False
            if events["condition"] == "Immediate":
                isLong = False
            elif events["condition"] == "Duration Long":
                isLong = True
            isConditionLong = isLong

            await self.access_manager.did_badge(
                badgeId=badgeId, reader=reader, isConditionLong=isConditionLong
            )
        elif events["event"] == "Code":
            code = events["code"]
            code_reader = data["deviceid"]
            await self.access_manager.code_is_given(code=code, reader=code_reader)

        elif events["condition"] == "Falling Edge":
            print("fall")

        elif events["condition"] == "Rising Edge":
            print("rise")

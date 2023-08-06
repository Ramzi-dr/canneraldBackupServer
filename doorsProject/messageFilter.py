
class MessageFilter:
    def __init__(self):
        pass

    def messageFilter(self, message):
        data = None

        if type(message) is dict:
            for key, value in message.items():
                if key == "params":
                    if value[0] == "ObservedStates":
                        data = value[1]["data"]
                        return data

        elif type(message) is list:
            if message[0] == "ObservedStates":
                data = message[1]["data"]

            return data

    def get_door_id(self, message):
        try:
            data = self.messageFilter(message)
            if data is not None:
                for key, value in data.items():
                    if key == "deviceid":
                        return data["deviceid"]
                    elif key == "modified":
                        return None
        except TypeError:
            return None

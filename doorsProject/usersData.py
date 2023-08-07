import json
import requests
from doorsProject.payloadCollection import PayloadCollection


class UsersData:
    def __init__(self):
        self.headers = PayloadCollection.headers
        self.url = PayloadCollection.canneraldRpcServerUrl
        self.codeList = self.getUserCode()
        self.mediaList = self.getMedia()
        self.masterUserList = self.getMasterUser()
        self.usersData = self.getUserData()

    def getMedia(self):
        response = requests.get(
            url=self.url,
            headers=self.headers,
            verify=True,
            data=PayloadCollection.media,
        )

        return json.loads(response.text)["result"]

    def getUserCode(self):
        url = PayloadCollection.canneraldRpcServerUrl
        response = requests.get(
            url=url, headers=self.headers, verify=True, data=PayloadCollection.code
        )

        return json.loads(response.text)["result"]

    def getMasterUser(self):
        response = requests.get(
            url=self.url,
            headers=self.headers,
            verify=True,
            data=PayloadCollection.master,
        )
        return json.loads(response.text)["result"]

    def getUserData(self):
        # Creating a dictionary to store the user information temporarily
        user_info_dict = {}

        # Adding codes to the user_info_dict
        for item in self.codeList:
            # print(item)
            userId = item["userId"]
            code = item["code"]
            if userId not in user_info_dict:
                user_info_dict[userId] = {
                    "userId": userId,
                    "media": [],
                    "code": [],
                    "Master": False,
                }
            user_info_dict[userId]["code"].append(code)

        # Adding media to the user_info_dict
        for item in self.mediaList:
            userId = item["userId"]
            media = item["publicMediaLabel"]
            if userId not in user_info_dict:
                user_info_dict[userId] = {
                    "userId": userId,
                    "media": [],
                    "code": [],
                    "Master": False,
                }
            user_info_dict[userId]["media"].append(media)

        # Adding Master to the user_info_dict
        for item in self.masterUserList:
            userId = item["baseId"]
            Master = item["value"]
            if userId not in user_info_dict:
                user_info_dict[userId] = {
                    "userId": userId,
                    "media": [],
                    "code": [],
                    "Master": Master,
                }
            user_info_dict[userId]["Master"] = Master

        # Converting the user_info_dict values to a list

        usersList = list(user_info_dict.values())
        usersData = []
        for user in usersList:
            if len(user["media"]) > 0 and len(user["code"]) > 0:
                usersData.append(user)
        print(usersData)
        return usersData


# user = UsersData().getUserData

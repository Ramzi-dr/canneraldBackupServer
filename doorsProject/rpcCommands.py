import requests
import json
from doorsProject.payloadCollection import PayloadCollection


def get_userLabel(user_id):
    response = requests.get(
        url=PayloadCollection.canneraldRpcServerUrl,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.userGroupRelations,
    )
    results = json.loads(response.text)["result"]
    for result in results:
        for key, value in result.items():
            if value == user_id:
                user_label = result["label"]
                return user_label


def get_userIdByMedia_info(publicMediaLabel):
    response = requests.get(
        url=PayloadCollection.canneraldRpcServerUrl,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.media,
    )
    results = json.loads(response.text)["result"]
    for result in results:
        for key, value in result.items():
            if value == publicMediaLabel:
                user_id = result["userId"]
                return user_id


def get_doorLabel(accessPointId):
    response = requests.get(
        url=PayloadCollection.canneraldRpcServerUrl,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.accessPoints,
    )
    results = json.loads(response.text)["result"]
    for result in results:
        for key, value in result.items():
            if value == accessPointId:
                doorLabel = result["label"]
                return doorLabel


def get_accessPointIdByReaderId_info(deviceId):
    response = requests.get(
        url=PayloadCollection.canneraldRpcServerUrl,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.devices,
    )
    results = json.loads(response.text)["result"]
    for result in results:
        for key, value in result.items():
            if value == deviceId:
                accessPointId = result["accessPointId"]
                return accessPointId


def activateReader_Ouput(readerId, outputNum):
    response = requests.get(
        url=PayloadCollection.canneraldRpcServerUrl,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.activate_output(deviceId=readerId, outputNum=outputNum),
    )
    results = json.loads(response.text)["result"]


def openDoor_short(deviceId, outputNum):
    url = PayloadCollection.canneraldRpcServerUrl
    response = requests.get(
        url=url,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.activate_output(deviceId=deviceId, outputNum=outputNum),
    )
    results = json.loads(response.text)["result"]
    print(results)


def openOrClose_door(deviceId, outputNum):
    url = PayloadCollection.canneraldRpcServerUrl
    response = requests.get(
        url=url,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.activate_output(deviceId=deviceId, outputNum=outputNum),
    )
    results = json.loads(response.text)["result"]
    print(results)

import requests
import json
from doorsProject.inputsState import getInputsState
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
        data=PayloadCollection.activate_output(
            deviceId=readerId, outputNum=outputNum, action=1
        ),
    )
    results = json.loads(response.text)["result"]


def openDoor_short(deviceId, outputNum):
    url = PayloadCollection.canneraldRpcServerUrl
    response = requests.get(
        url=url,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.activate_output(
            deviceId=deviceId, outputNum=outputNum, action=1
        ),
    )
    results = json.loads(response.text)["result"]
    print(results)


def openOrClose_door(deviceId, outputNum):
    def relayToggle():
        # this function is only for relay 1 , u have to change the outputNum to make it flexible
        action = None
        if (
            getInputsState(deviceId=deviceId) == 1
            or getInputsState(deviceId=deviceId) == 3
        ):
            # state 1 = relay1 is active /state 2 = relay2 is active / state 3 = relay1 and 2 are active
            action = 16
            openAction = 4
            closeAction = 16
        elif (
            getInputsState(deviceId=deviceId) == 0
            or getInputsState(deviceId=deviceId) == 2
        ):
            action = 4
        print(action)
        return action

    relayToggle()

    url = PayloadCollection.canneraldRpcServerUrl
    response = requests.get(
        url=url,
        headers=PayloadCollection.headers,
        verify=True,
        data=PayloadCollection.activate_output(
            deviceId=deviceId,
            outputNum=outputNum,
            action=relayToggle(),
        ),
    )

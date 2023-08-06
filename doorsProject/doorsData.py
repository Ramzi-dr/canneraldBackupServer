import json
import requests
from doorsProject.payloadCollection import PayloadCollection


class DoorsData:
    def __init__(self):
        self.headers = PayloadCollection.headers
        self.url = PayloadCollection.canneraldRpcServerUrl
        self.doorsData = self.getDoorsPropertyData()

    def getAccessPointsWithTwoFactorAuthenticationId(self):
        accessPointIdList = []
        response = requests.get(
            url=self.url,
            headers=self.headers,
            verify=True,
            data=PayloadCollection.accessPointPropertyData,
        )
        results = json.loads(response.text)["result"]
        for result in results:
            for key, value in result.items():
                if {key: value} == {
                    "propertyId": PayloadCollection.towFactorAuthenticationId
                }:
                    for key, value in result.items():
                        if {key: value} == {"value": True} or {key: value} == {
                            "value": "1"
                        }:
                            baseId = result["baseId"]
                            accessPointIdList.append(baseId)
        return accessPointIdList

    def getDoorsPropertyData(self):
        accessPointIdList = self.getAccessPointsWithTwoFactorAuthenticationId()
        response = requests.get(
            url=self.url,
            headers=self.headers,
            verify=True,
            data=PayloadCollection.devices,
        )

        results = json.loads(response.text)["result"]
        accessPointDevices = {}
        for result in results:
            for accessPointId in accessPointIdList:
                if result["accessPointId"] == accessPointId:
                    list_of_dicts = [result]
                    for item in list_of_dicts:
                        access_point_id = item["accessPointId"]
                        device_type = item["deviceType"]
                        device_id = item["deviceid"]
                        if device_type == 103:
                            accessPointDevices.setdefault(
                                access_point_id, {}
                            ).setdefault("IO_Module", []).append(device_id)
                        if device_type == 80:
                            accessPointDevices.setdefault(
                                access_point_id, {}
                            ).setdefault("IO_Extender", []).append(device_id)
                        elif device_type == 101 or device_type == 102:
                            accessPointDevices.setdefault(
                                access_point_id, {}
                            ).setdefault("E_Reader", []).append(device_id)

        return accessPointDevices

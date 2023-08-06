import json
import os
import time


class PayloadCollection:
    username = os.environ.get("GLUTZ_BST_USER")
    password = os.environ.get("GLUTZ_BST_PASS")
    headers = {"Content-Type": "application/json"}
    GlutzUrl = "31.24.10.138"
    eventWsServerPort = 8750
    eventWsServerIp = "localhost"
    eventWsServerUrl = f"ws://{eventWsServerIp}:{eventWsServerPort}"
    localWsServerPort = 8800
    localWsServerIp = "localhost"
    localWsServerIp = f"ws://{localWsServerIp}:{localWsServerPort}"
    canneraldRpcServerUrl = f"http://{username}:{password}@{GlutzUrl}:8332/rpc/"
    canneraldWsServerUrl = f"ws://{username}:{password}@{GlutzUrl}:8332"
    # lagerHausServerGlutzUrl = 'lagerhausweg-10.onlinezuko.ch'
    # canneraldGlutzUrl = 'werk-fraubrunnen.onlinezuko.ch'
    # canneraldRpcServerUrl = (
    #    f"https://{username}:{password}@werk-fraubrunnen.onlinezuko.ch/rpc/"
    # )
    # lagerHausRpcServerUrl = (
    #   f"https://{username}:{password}@lagerhausweg-10.onlinezuko.ch/rpc/"
    # )
    towFactorAuthenticationId = "5022"
    IO_Module_Type = 103
    E_Reader_IP55_Type = 102
    E_Reader_Type = 101
    IO_Extender_Type = 80
    message = {
        "method": "registerObserver",
        "params": [
            [
                "UsersGroups",
                "UserGroupRelations",
                "Codes",
                "Media",
                "Devices",
                "AccessPoints",
                "AuthorizationPoints",
                "AuthorizationPointRelations",
                "DeviceEvents",
                "Rights",
                "ObservedStates",
                "TimeProfiles",
                "TimeSlots",
                "DeviceStatus",
                "RouteTree",
                "Properties",
                "PropertyValueSpecs",
                "DevicePropertyData",
                "DeviceStaticPropertyData",
                "SystemPropertyData",
                "AccessPointPropertyData",
                "UserPropertyData",
                "HolidayCalendars",
                "Holidays",
                "DeviceUpdates",
                "EventLog",
                "CustomProperties",
                "Logins",
                "ActionProfiles",
                "PermissionProfiles",
                "Permissions",
                "Subsystems",
                "CustomFilesTree",
            ]
        ],
        "jsonrpc": "2.0",
    }
    userGroupRelations = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["UsersGroups", {}, ["id", "subsystemId", "label", "class"]],
            "id": 9,
            "jsonrpc": "2.0",
        }
    )

    @staticmethod
    def activate_output(deviceId, outputNum):
        payload = json.dumps(
            {
                "method": "eAccess.deviceOperation",
                "params": [
                    "OpenDoor",
                    {
                        "deviceid": deviceId,
                        "action": 1,
                        "outputs": outputNum,
                        "hasMotor": "false",
                    },
                ],
                "id": 61,
                "jsonrpc": "2.0",
            }
        )
        return payload

    getAuthorizationPointProperty = json.dumps(
        {
            "method": "eAccess.getAuthorizationPointProperty",
            "params": [
                "propertyName",
                {},
                [],
            ],
            "id": 16,
            "jsonrpc": "2.0",
        }
    )

    devices = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": [
                "Devices",
                {},
                ["id", "label", "deviceid", "deviceType", "accessPointId", "roles"],
            ],
            "id": 8,
            "jsonrpc": "2.0",
        }
    )
    accessPointPropertyData = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["AccessPointPropertyData", {}, []],
            "id": 2,
            "jsonrpc": "2.0",
        }
    )
    accessPoints = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["AccessPoints", {}, ["id", "label", "function"]],
            "id": 8,
            "jsonrpc": "2.0",
        }
    )
    media = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": [
                "Media",
                {},
                [
                    "id",
                    "userId",
                    "actionProfileId",
                    "uid",
                    "publicMediaLabel",
                    "description",
                    "validFrom",
                    "validTo",
                    "mediumType",
                    "technicalMediaId",
                ],
            ],
            "id": 8,
            "jsonrpc": "2.0",
        }
    )
    code = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": [
                "Codes",
                {},
                [
                    "id",
                    "userId",
                    "actionProfileId",
                    "code",
                    "description",
                    "validFrom",
                    "validTo",
                ],
            ],
            "id": 9,
            "jsonrpc": "2.0",
        }
    )

    master = json.dumps(
        {
            "method": "eAccess.getModel",
            "params": ["UserPropertyData", {}],
            "id": 26,
            "jsonrpc": "2.0",
        }
    )

    @staticmethod
    def getAccessPoint():
        payload = json.dumps(
            {
                "method": "eAccess.getModel",
                "params": [
                    "Rights",
                    {},
                    [
                        "id",
                        "userId",
                        "authorizationPointId",
                        "timeProfileId",
                        "validFrom",
                        "validTo",
                        "actions",
                        "options",
                    ],
                ],
                "id": 16,
                "jsonrpc": "2.0",
            }
        )
        return payload

    def count_seconds(duration):
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < duration:
            elapsed_time = time.time() - start_time
            time.sleep(1)  # Wait for 1 second
        print(int(elapsed_time))
        return elapsed_time

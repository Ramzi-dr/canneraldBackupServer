import json
import os


class PayloadCollection:
    username = os.environ.get("GLUTZ_BST_USER")
    password = os.environ.get("GLUTZ_BST_PASS")
    headers = {"Content-Type": "application/json"}
    GlutzUrl = "31.24.10.138"
    # localWsServerPort = 8750
    # localWsServerUrl = f"ws://localhost:{localWsServerPort}"
    canneraldRpcServerUrl = f"http://{username}:{password}@{GlutzUrl}:8332/rpc/"
    canneraldWsServerUrl = f"ws://{username}:{password}@{GlutzUrl}:8332"
    backupWsServerPort = 8800
    backupWsServerIp = "localhost"
    backupWsServerUrl = f"ws://{backupWsServerIp}:{backupWsServerPort}"
    towFactorAuthenticationId = "5022"  # in Glutz door Properties
    IO_Module_Type = 103
    E_Reader_IP55_Type = 102
    E_Reader_Type = 101
    IO_Extender_Type = 80
    IO_ModuleRelay_1 = 2
    IO_ModuleRelay_2 = 4
    masterCodeActionProfileId = 1002

    masterCodeActionProfileId = 1002  # in Glutz Codes menu profile non Default
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
    def activate_output(deviceId, outputNum, action):
        payload = json.dumps(
            {
                "method": "eAccess.deviceOperation",
                "params": [
                    "OpenDoor",
                    {
                        "deviceid": deviceId,
                        "action": action,
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

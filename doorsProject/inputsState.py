import jsonrpclib
from doorsProject.emailManager import sendGmail_ramziVersion
from doorsProject.payloadCollection import PayloadCollection


def getInputsState(deviceId):
    try:
        server = jsonrpclib.Server(PayloadCollection.canneraldRpcServerUrl)
        output = server.eAccess.getModel("AccessPointLocations")

        eAccess = server.eAccess.deviceOperation(
            "TestInputState",
            {
                "deviceid": deviceId,
            },
        )
        state = eAccess["state"]

        return state
    except Exception as e:
        sendMail_afterException(exeption=e)
        print(e)


def sendMail_afterException(exeption):
    try:
        sendGmail_ramziVersion(
            f"Error in inputsState file \nError: {exeption}",
            subject="hallo from  event server .",
        )
    except Exception as e:
        print(e)
        pass

import jsonrpclib
from payloadCollection import PayloadCollection

# server = jsonrpclib.Server('http://admin:admin@localhost:8332/rpc/')
# # print(server.eAccess.getModel('AccessPointLocations'))
# eAccess = server.eAccess.deviceOperation("TestInputState", {"deviceid": "566.890.768", })
# # input_result = int(eAccess["state"])
# #print(eAccess["state"])
# input_status = eAccess["state"]+ eAccess['errorCode']
server = jsonrpclib.Server(PayloadCollection.canneraldRpcServerUrl)
output = server.eAccess.getModel("AccessPointLocations")
# for accessPoint in output:
#     for key, value in accessPoint.items():
#         if value == 'Mieter Cannerald':
#             print(accessPoint['nodes'])

eAccess = server.eAccess.deviceOperation(
    "TestInputState",
    {
        "deviceid": "566.890.768",
    },
)
print(eAccess)

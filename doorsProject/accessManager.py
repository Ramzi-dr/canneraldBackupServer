from doorsProject.doorsData import DoorsData
from doorsProject.usersData import UsersData
from doorsProject.rpcAction import RpcAction
import asyncio
import time


class AccessManager:
    def __init__(self, doors_instances, delete_door_instance_function):
        self.doors_instances = doors_instances
        self.delete_door_instance = delete_door_instance_function
        self.doorsData = None
        self.usersData = None
        self.reader = None
        self.is_Master = False
        self.ListOf_IO_Module = None
        self.ListOf_IO_Extender = None
        self.code = None
        self.badgeId = None
        self.conditionLong = False
        self.timer_running = False
        self.timer_start_time = None
        self.timer_duration = None
        self.timer_thread = None
        self.seconds = 20
        self.rpc_action = RpcAction()

    async def _get_doorsAndUsers_data(self):
        self.doorsData = DoorsData().doorsData
        self.usersData = UsersData().usersData
        print(self.doorsData)

    async def _start_timer(self):
        while self.timer_running:
            current_time = time.time()
            elapsed_time = current_time - self.timer_start_time
            self.rpc_action.activate_Reader_Output(readerId=self.reader)
            print('please give ur code now')
            if elapsed_time >= self.timer_duration:
                self.timer_running = False
                print('sorry ur time is out')
            else:
                time_to_sleep = min(1, self.timer_duration - elapsed_time)
                await asyncio.sleep(time_to_sleep)

    async def did_badge(self, badgeId, reader, isConditionLong):
        print('user did badge')
        await self._get_doorsAndUsers_data()
        self.badgeId = badgeId
        self.reader = reader
        self.conditionLong = isConditionLong

        if await self.reader_exist(reader=reader):
            if await self.door_have_outputDevice(reader=reader):
                if self.timer_running:
                    # Timer is already running, so reset it
                    print('timer is running and is reset')
                    self.timer_running = False
                self.timer_duration = self.seconds
                self.timer_start_time = time.time()
                self.timer_running = True
                print('timer is running now')
                await asyncio.gather(self._start_timer())

    async def code_is_given(self, code, reader):
        self.code = code
        print('code is given')
        if not self.timer_running:
            print('u have to use ur badge first')
            return
        if self.timer_running:
            # The second method is called while the timer is still running
            if self.reader == reader:
                if self.same_CodeAndBadge_user():
                    self.timer_running = False
                    self.code = code
                    print('timer is stopped')
                    self.give_access(door_id=reader)

    async def door_have_outputDevice(self, reader):
        haveOutputDevice = False
        for doorId, doorDevices in self.doorsData.items():

            if reader in doorDevices['E_Reader']:
                for key, value in doorDevices.items():

                    if key == 'IO_Module':

                        if value:
                            haveOutputDevice = True
                            self.ListOf_IO_Module = value

                    if key == 'IO_Extender':

                        if value:
                            haveOutputDevice = True
                            self.ListOf_IO_Extender = value

        print(haveOutputDevice)
        return haveOutputDevice

    async def reader_exist(self, reader):
        deviceId_found = False
        for key, value in self.doorsData.items():
            for device, deviceId in value.items():
                if device == 'E_Reader':
                    for my_id in deviceId:
                        if my_id == reader:
                            deviceId_found = True
        return deviceId_found

    def same_CodeAndBadge_user(self):
        is_theSameUser = False
        for user in self.usersData:
            for user_code in user['code']:
                if user_code == self.code:
                    for badge in user['media']:
                        if badge == self.badgeId:
                            is_theSameUser = True
                        if user['Master'] == '1' or user['Master'] is True:
                            self.is_Master = True
        return is_theSameUser

    def give_access(self, door_id):
        self.delete_door_instance(door_id=door_id)  # Call the delete_door_instance function
        if self.ListOf_IO_Extender is None:

            if self.conditionLong:
                self.rpc_action.activate_IO_Output(IO_Module=self.ListOf_IO_Module[0], activationModus='open',
                                                   media=self.badgeId, readerId=door_id)
            else:
                self.rpc_action.activate_IO_Output(IO_Module=self.ListOf_IO_Module[0], media=self.badgeId,
                                                   readerId=door_id)
        else:
            if self.conditionLong:
                self.rpc_action.activate_IO_Output(IO_Module=self.ListOf_IO_Extender[0], activationModus='open',
                                                   media=self.badgeId, readerId=door_id)
            else:
                self.rpc_action.activate_IO_Output(IO_Module=self.ListOf_IO_Extender[0], media=self.badgeId,
                                                   readerId=door_id)

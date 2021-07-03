from Service import Service 
import json
import sys
import requests
from MySim import MySim
from MyShop import ContextType
from MySim import MySim
import time

class SimNode(Service):

    def __init__(self, name, thisPort):
        Service.__init__(self, name, thisPort)
        self.mySimMap = {}
    
    def Execute(self, parameters):
        if 'content' in parameters and 'url' in parameters:
            url = parameters['url']
            package = json.loads(parameters['content'])

            if url == '/Connect':
                if 'setting' in package and 'user' in package:
                    user = package['user']
                    setting = package['setting']
                    if self.mySimMap.get(user) == None:
                        mySim = MySim()
                        self.mySimMap[user] = mySim
                        mySim.Initialize(setting)
                        print('Initialized')
                return None

            if url == '/ChangeBatch':
                if 'wip' in package and 'batch' in package and 'user' in package:
                    user = package['user']
                    if self.mySimMap.get(user) != None:
                        mySim = self.mySimMap[user]
                        wip = package['wip']
                        batch = package['batch']
                        rule = mySim.GetRule()
                        rule.ChangeBatch(wip, batch)
                return None

            if url == '/ChangePriority':
                if 'wip' in package and 'priority' in package and 'user' in package:
                    user = package['user']
                    if self.mySimMap.get(user) != None:
                        mySim = self.mySimMap[user]
                        wip = package['wip']
                        priority = package['priority']
                        rule = mySim.GetRule()
                        rule.ChangePriority(wip, priority)
                        mySim.Change()
                return None

            if url == '/RunStep' and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    mySim.RunStep()
                return None

            if url == '/Run' and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    mySim.Run()
                return None

            if url == "/GetOfflineData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    OfflineData = mySim.GetOfflineData()
                    return OfflineData
                return None

            if url == "/GetOnlineData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    onlineData = mySim.GetOnlineData()
                    return onlineData
                return None

            if url == "/GetRunningData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    runningData = mySim.GetRunningData()
                    return runningData
                return None

            if url == "/GetTick" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    return mySim.tick
                return None

            # 添加读取在制品、机床表的API，以便客户端获取仿真数据
            if url == "/GetWipData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    shop = mySim.GetShop()
                    return shop.GetWipData()
                return None
            
            if url == "/GetMachineData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    shop = mySim.GetShop()
                    return shop.GetMachineData()
                return None

            if url == "/GetFinishedData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    return mySim.GetFinishedMap()
                return None

            if url == "/GetEvents" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    return mySim.GetEvents()
                return None
        
        return None


if __name__ == '__main__':

    servicePort = "21560"
    serviceName = "MyShop"

    services = SimNode(serviceName, servicePort)

    print('RUNNING')
    services.Run()
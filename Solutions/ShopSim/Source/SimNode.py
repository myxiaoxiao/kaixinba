from Service import Service 
import json
import sys
import requests
from MySim import MySim
from MyShop import ContextType
from MySim import MySim
import time

class SimNode(Service):

    def __init__(self, name, thisPort, nodePort):
        Service.__init__(self, name, thisPort, nodePort)
        # one user for one simulation
        self.mySimMap = {}
    
    def Execute(self, parameters):
        if 'content' in parameters and 'url' in parameters:
            url = parameters['url']
            package = json.loads(parameters['content'])

            if url == 'Connect':
                if 'setting' in package and 'user' in package:
                    user = package['user']
                    setting = package['setting']
                    if self.mySimMap.get(user) == None:
                        mySim = MySim()
                        self.mySimMap[user] = mySim
                        mySim.Initialize(setting)
                return None

            if url == 'ChangeBatch':
                if 'wip' in package and 'batch' in package and 'user' in package:
                    user = package['user']
                    if self.mySimMap.get(user) != None:
                        mySim = self.mySimMap[user]
                        wip = package['wip']
                        batch = package['batch']
                        rule = mySim.GetRule()
                        rule.ChangeBatch(wip, batch)
                return None

            if url == 'ChangePriority':
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

            if url == 'RunStep' and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    mySim.RunStep()
                return None

            if url == 'Run' and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    mySim.Run()
                return None

            if url == "GetOfflineData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    OfflineData = mySim.GetOfflineData()
                    return OfflineData
                return None

            if url == "GetOnlineData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    onlineData = mySim.GetOnlineData()
                    return onlineData
                return None

            if url == "GetRunningData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    runningData = mySim.GetRunningData()
                    return runningData
                return None

            if url == "GetTick" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    return mySim.tick
                return None

            # 备忘录 2020-02-27
            # 添加读取在制品、机床表的API，以便客户端获取仿真数据
            if url == "GetWipData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    shop = mySim.GetShop()
                    return shop.GetWipData()
                return None
            
            if url == "GetMachineData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    shop = mySim.GetShop()
                    return shop.GetMachineData()
                return None

            if url == "GetFinishedData" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    return mySim.GetFinishedMap()
                return None

            if url == "GetEvents" and 'user' in package:
                user = package['user']
                if self.mySimMap.get(user) != None:
                    mySim = self.mySimMap[user]
                    return mySim.GetEvents()
                return None
        
        return None

# 备忘录 2020-02-21
# 启动主线程监听外部事件
# 启动一个子线程进行模拟仿真
# 外部客户端通过接口控制模拟过程
# 
# Connect simulation
# Post : Connect
# 
# loop call below to run simulation
# ------------------start step-------------------------------
# do some change for next step
# 
# Post : ChangeBatch if need
# Post : ChangePriority if need
# -------------------------------------------------
# Post : RunStep
# -------------------------------------------------
# Post : GetOfflineData
# Post : GetOnlineData
# savig if need
# 
# ------------------end step-------------------------------

if __name__ == '__main__':
    # servicePort = sys.argv[1]
    # nodePort = sys.argv[2]
    # serviceName = sys.argv[3]

    servicePort = "21561"
    nodePort = "21560"
    serviceName = "MyShop"

    print(serviceName + ' STARTED')
    print('PORT : ' + servicePort)

    services = SimNode(serviceName, servicePort, nodePort)

    print('ADD APIS...')
    print('API : Connect')
    services.Append('Connect')
    print('API : ChangeBatch')
    services.Append('ChangeBatch')
    print('API : ChangePriority')
    services.Append('ChangePriority')
    print('API : RunStep')
    services.Append('RunStep')
    print('API : GetOfflineData')
    services.Append('GetOfflineData')
    print('API : GetOnlineData')
    services.Append('GetOnlineData')
    print('API : GetWipData')
    services.Append('GetWipData')
    print('API : GetMachineData')
    services.Append('GetMachineData')
    print('API : GetFinishedData')
    services.Append('GetFinishedData')
    print('API : GetTick')
    services.Append('GetTick')
    print('API : Run')
    services.Append('Run')
    print('API : GetRunningData')
    services.Append('GetRunningData')
    print('API : GetEvents')
    services.Append('GetEvents')

    print('RUNNING')
    services.Run()
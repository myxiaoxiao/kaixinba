from Service import Service 
import json
import sys
import requests
import time

class SimNode(Service):

    def __init__(self, name, thisPort, nodePort):
        Service.__init__(self, name, thisPort, nodePort)
        self.mySimMap = {}
    
    def Execute(self, parameters):
        if 'content' in parameters and 'url' in parameters:
            url = parameters['url']
            package = json.loads(parameters['content'])

            # if url == 'Connect':
            #     if package.get('setting'):
            #         setting = package['setting']
            #         self.mySim.Initialize(setting)
            #         return None

            # if url == 'ChangeBatch':
            #     if package.get('wip') and package.get('batch'):
            #         wip = package['wip']
            #         batch = package['batch']
            #         rule = self.mySim.GetRule()
            #         rule.ChangeBatch(wip, batch)
            #         return None

            # if url == 'ChangePriority':
            #     if package.get('wip') and package.get('priority'):
            #         wip = package['wip']
            #         priority = package['priority']
            #         rule = self.mySim.GetRule()
            #         rule.ChangePriority(wip, priority)
            #         self.mySim.Change()
            #         return None

            # if url == 'RunStep':
            #     self.mySim.RunStep()
            #     return None

            # if url == "GetOfflineData":
            #     OfflineData = self.mySim.GetOfflineData()
            #     return OfflineData

            # if url == "GetOnlineData":
            #     onlineData = self.mySim.GetOnlineData()
            #     return onlineData

            # if url == "GetTick":
            #     return self.mySim.tick

            # # 备忘录 2020-02-27
            # # 添加读取在制品、机床表的API，以便客户端获取仿真数据
            # if url == "GetWipData":
            #     shop = self.mySim.GetShop()
            #     return shop.GetWipData()
            
            # if url == "GetMachineData":
            #     shop = self.mySim.GetShop()
            #     return shop.GetMachineData()

            # if url == "GetFinishedData":
            #     return self.mySim.GetFinishedMap()
        
        return None

if __name__ == '__main__':
    # servicePort = sys.argv[1]
    # nodePort = sys.argv[2]
    # serviceName = sys.argv[3]

    servicePort = "21563"
    nodePort = "21560"
    serviceName = "MyRobot"

    print(serviceName + ' STARTED')
    print('PORT : ' + servicePort)

    services = SimNode(serviceName, servicePort, nodePort)

    # print('ADD APIS...')
    # print('API : Connect')
    # services.Append('Connect')
    # print('API : ChangeBatch')
    # services.Append('ChangeBatch')
    # print('API : ChangePriority')
    # services.Append('ChangePriority')
    # print('API : RunStep')
    # services.Append('RunStep')
    # print('API : GetOfflineData')
    # services.Append('GetOfflineData')
    # print('API : GetOnlineData')
    # services.Append('GetOnlineData')
    # print('API : GetWipData')
    # services.Append('GetWipData')
    # print('API : GetMachineData')
    # services.Append('GetMachineData')
    # print('API : GetFinishedData')
    # services.Append('GetFinishedData')
    # print('API : GetTick')
    # services.Append('GetTick')

    print('RUNNING')
    services.Run()
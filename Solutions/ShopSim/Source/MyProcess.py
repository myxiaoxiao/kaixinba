from MyData import MyData

class MyProcess(MyData):
    def __init__(self, number, nextProcess, index, setup, duration, teardown, wip, dispersed, machineCapacityMap):
        MyData.__init__(self)
        self.SetNumber(number)
        self.asset['machineCapacityMap'] = machineCapacityMap # 该工艺在每个能加工该工艺的机床上一次能加工多少零件(key是machineNumber, value是capacity)
        self.asset['next'] = nextProcess # 下一个工序
        self.asset['index'] = index # 序号
        self.asset['setup'] = setup # 装夹时间
        self.asset['duration'] = duration # 加工时间
        self.asset['teardown'] = teardown # 拆卸时间
        self.asset['wip'] = wip # 在制品的编号
        self.asset['dispersed'] = dispersed # 是否离散

    def GetNext(self):
        return self.asset['next']

    def GetSetup(self):
        return self.asset['setup']
        
    def GetDuration(self):
        return self.asset['duration']

    def GetTeardown(self):
        return self.asset['teardown']

    def GetWip(self):
        return self.asset['wip']

    def GetMachineCapacityMap(self):
        return self.asset['machineCapacityMap']

    def IsDispersed(self):
        return self.asset['dispersed']

    def GetIndex(self):
        return self.asset['index']

    def GetCapacity(self, machineNumber):
        return self.asset['machineCapacityMap'][machineNumber]
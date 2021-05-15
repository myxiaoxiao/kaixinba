from MyProcess import MyProcess
from MyWip import MyWip
from MyMachine import MyMachine
from MyTypes import ContextType

class MyShop:
    def __init__(self):
        self.machineMap = {} #机床字典
        self.processMap = {} #工艺字典
        self.wipMap = {} #在制品字典
        self.machineWipsMap = {} #“机床能加工哪些在制品”字典
        self.partWipsMap = {} #“一个零件拥有哪些在制品”字典
    
    #输出所有的在制品信息
    def GetWipData(self):
        wipData = {}
        for wipNumber in self.wipMap:
            wip = self.wipMap[wipNumber]
            wipData[wipNumber] = wip.ToData()
        return wipData
    
    #输出所有的机床信息
    def GetMachineData(self):
        machineData = {}
        for machineNumber in self.machineMap:
            machine = self.machineMap[machineNumber]
            machineData[machineNumber] = machine.ToData()
        return machineData

    #输出对象
    def GetObject(self, contextType, number):
        dataMap = self.GetContext(contextType)
        if dataMap == None:
            return None
            
        if number in dataMap:
            return dataMap[number]
        else:
            return None

    #输出对应类型对象的字典
    def GetContext(self, contextType):
        dataMap = None
        if contextType == ContextType.MACHINE:
            dataMap = self.machineMap
        elif contextType == ContextType.PROCESS:
            dataMap = self.processMap
        elif contextType == ContextType.WIP:
            dataMap = self.wipMap
        return dataMap
    
    #初始化所有的字典
    def Initialize(self, setting):
        self.InitializeMachineMap(setting)
        self.InitializeWipMap(setting)
        self.InitializeProcessMap(setting)
        self.InitializeMachineWipsMap()

    #初始化机床字典
    def InitializeMachineMap(self, setting):
        if 'machines' in setting:
            machines = setting['machines']
            for it in machines:
                machineNumber = it['number']
                machine = MyMachine(machineNumber)
                self.machineMap[machineNumber] = machine

    #初始化在制品字典
    def InitializeWipMap(self, setting):
        if 'wips' in setting:
            wips = setting['wips']
            for it in wips:
                wipNumber = it['number']
                quantity = it['quantity']
                part = it['part']
                wip = MyWip(wipNumber, quantity, part)
                self.wipMap[wipNumber] = wip

    #初始化工艺字典
    def InitializeProcessMap(self, setting):
        if 'processes' in setting:
            processes = setting['processes']
            partIndexMap = {}
            for it in processes:
                machineCapacityMap = it['machineCapacityMap']
                processNumber = it['number']
                nextProcess = it['next']
                setup = it['setup']
                duration = it['duration']
                teardown = it['teardown']
                wipNumber = it['wip']
                dispersed = it['dispersed']

                wip = self.GetObject(ContextType.WIP, wipNumber)
                part = wip.GetPart()
                if part not in partIndexMap:
                    partIndexMap[part] = 0
                else:
                    partIndexMap[part] = partIndexMap[part] + 1
                index = partIndexMap[part]

                process = MyProcess(processNumber, nextProcess, index, setup, duration, teardown, wipNumber, dispersed, machineCapacityMap)
                self.processMap[processNumber] = process
                wip.SetProcess(processNumber)
                # 算法备忘录 2020-02-29
                # partWipsMap 的定义如下
                # 键是零件编号
                # 值是在制品编号按零件工序排序的列表
                if part not in self.partWipsMap:
                    self.partWipsMap[part] = []
                self.partWipsMap[part].append(wipNumber)

    #初始化“机床能加工哪些在制品”字典
    def InitializeMachineWipsMap(self):
        # 算法备忘录
        # 遍历所有的机床，建立机床和wips的表
        # 对每一个机床收集工艺的机床集合中包含该机床的工艺
        for machineNumber in self.machineMap:
            wipNumbers = {}
            processMap = self.GetContext(ContextType.PROCESS)
            for processNumber in processMap:
                process = processMap[processNumber]
                machineCapacityMap = process.GetMachineCapacityMap()
                if machineNumber not in machineCapacityMap:
                    continue
                wipNumber = process.GetWip()
                wipNumbers[wipNumber] = wipNumber
            self.machineWipsMap[machineNumber] = wipNumbers

    #查询在制品能否在机床上工作
    def IsOnMachine(self, machineNumber, wipNumber):
        if machineNumber not in self.machineWipsMap:
            return False
        wips = self.machineWipsMap[machineNumber]
        if wipNumber not in wips:
            return False
        return True

    #查询在此在制品之前还有没有零件加工完的
    def HasWipComingFlow(self, theWipNumber):
        theWip = self.GetObject(ContextType.WIP, theWipNumber)
        part = theWip.GetPart()
        wips = self.partWipsMap[part]
        count = 0
        for wipNumber in wips:
            if theWipNumber == wipNumber:
                return False
            else:
                wip = self.GetObject(ContextType.WIP, wipNumber)
                count = count + wip.GetQuantity()
                if count > 0:
                    process = self.GetObject(ContextType.PROCESS, wip.GetProcess())
                    if process.IsDispersed() == True:
                        return True
                    else:
                        return False
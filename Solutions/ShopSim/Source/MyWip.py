from MyData import MyData
from MyProcess import MyProcess
from MyTypes import ContextType

# wip is the parts in one process
#在制品等候区
class MyWip(MyData):
    def __init__(self, number, quantity, part):
        MyData.__init__(self)
        self.SetNumber(number)
        # 在制品工艺
        self.asset['process'] = ''
        # 在制品数量
        self.asset['quantity'] = quantity
        # 在制品零件号
        self.asset['part'] = part
        self.timeline = []

    # 挪到下一个在制品区
    def MoveToNextWip(self, simulation, tick, shop, count):
        nextProcess = self.GetNextProcess(shop)
        if nextProcess != None:
            nextWipNumber = nextProcess.GetWip()
            nextWip = shop.GetObject(ContextType.WIP, nextWipNumber)
            nextWip.Checkin(simulation, shop, tick, count)

    # 获取工艺编号
    def GetProcess(self):
        return self.asset['process']
    # 设置工艺编号
    def SetProcess(self, processNumber):
        self.asset['process'] = processNumber

    # 获取在制品数量
    def GetQuantity(self):
        return self.asset['quantity']
    
    # 获取在制品零件号
    def GetPart(self):
        return self.asset['part']

    # 从在制品挪零件出去
    def Checkout(self, simulation, shop, tick, count):
        self.asset['quantity'] = self.asset['quantity'] - count
        # print("wip checkout " + str(count))
        self.DoPrint()
        self.Append(tick, self.asset['quantity'])

        processNmuber = self.GetProcess()
        process = shop.GetObject(ContextType.PROCESS, processNmuber)
        if process.GetIndex() == 0:
            event = {}
            event['location'] = 'material'
            event['time'] = tick
            event['number'] = self.asset['number']
            event['description'] = self.asset['part'] + "/checkout " + str(count)
            simulation.AddEvent(event)
        else:
            event = {}
            event['location'] = 'wip'
            event['time'] = tick
            event['number'] = self.asset['number']
            event['description'] = self.asset['number'] + "/checkout " + str(count)
            simulation.AddEvent(event)
    
    # 从外面挪零件进来
    def Checkin(self, simulation, shop, tick, count):
        self.asset['quantity'] = self.asset['quantity'] + count
        # print("wip Checkin " + str(count))
        self.DoPrint()
        self.Append(tick, self.asset['quantity'])

        processNmuber = self.GetProcess()
        process = shop.GetObject(ContextType.PROCESS, processNmuber)
        if process.GetIndex() == 0:
            event = {}
            event['location'] = 'material'
            event['time'] = tick
            event['number'] = self.asset['number']
            event['description'] = self.asset['number'] + "/checkin " + str(count)
            simulation.AddEvent(event)
        else:
            event = {}
            event['location'] = 'wip'
            event['time'] = tick
            event['number'] = self.asset['number']
            event['description'] = self.asset['number'] + "/checkin " + str(count)
            simulation.AddEvent(event)


    # 得到下一个工艺对象
    # 输入参数 shop : 工厂对象
    # 输出下一个工艺对象
    def GetNextProcess(self, shop):
        processNmuber = self.asset['process']
        process = shop.GetObject(ContextType.PROCESS, processNmuber)
        nextProcessNumber = process.GetNext()
        nextProcess = shop.GetObject(ContextType.PROCESS, nextProcessNumber)
        return nextProcess
    
    def Append(self, tick, quantity):
        item = {}
        item['tick'] = tick
        item['quantity'] = quantity
        self.timeline.append(item)

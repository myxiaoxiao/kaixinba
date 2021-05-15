from MyData import MyData
from MyShop import ContextType
from MyTypes import TaskStatus
import time

# 任务按优先级分三个等级
# 1. 特别紧急 : 所有的生产资料（机床、人员、刀具等等）都最高优先无条件服务于此类零件
# 2. 一般紧急 : 在生产资料合理分配的前提下，尽量优先满足此类零件的生产
# 3. 不紧急   : 在满足生产优化下的前提下，获得生产资料用于零件的生产

# task combine machine, part(one instance of wip), tools
class MyTask(MyData):#任务
    def __init__(self, tick, wipNumber, machineNumber, batch):#时间，在制品编号 ，机床编号，一批生产的量
        MyData.__init__(self)
        self.SetNumber(machineNumber + '&' + str(int(round(time.time() * 1000))))
        self.asset['machine'] = machineNumber #机床编号
        self.asset['wip'] = wipNumber #在制品编号
        self.asset['batch'] = batch #最小经济批量
        self.asset['kickoff'] = tick  #每一个零件的开始时间（冷加工）
        self.asset['status'] = TaskStatus.SETUP #状态
        self.asset['index'] = 0 #正在加工零件的序号
        self.asset['costs'] = [] #每一个零件花费时间
        self.asset['begin'] = tick

    # 输出开始时间
    def GetKickoff(self):
        return self.asset['kickoff']
    #输出在制品编号
    def GetWip(self):
        return self.asset['wip']
    #完成零件
    def FinishPart(self, simulation, tick, shop, inserted):
        wipNumber = self.asset['wip']
        wip = shop.GetObject(ContextType.WIP, wipNumber)

        processNumber = wip.GetProcess()
        process = shop.GetObject(ContextType.PROCESS, processNumber)

        machineNumber = self.asset['machine']
        capacity = process.GetCapacity(machineNumber)
        leftCount = self.asset['batch'] - self.asset['index']

        runningCount = 0
        if leftCount >= capacity:
            runningCount = capacity
        else:
            runningCount = leftCount
        leftCount = leftCount - runningCount

        self.asset['status'] = TaskStatus.SETUP
        self.asset['index'] = self.asset['index'] + runningCount
        
        cost = tick - self.asset['kickoff']
        self.asset['costs'].append(cost)

        wip.MoveToNextWip(simulation, tick, shop, runningCount)
        if inserted == True:#插单
            self.asset['status'] = TaskStatus.RELEASE
            # print("release task")
            self.DoPrint()

            event = {}
            event['location'] = 'machine'
            event['time'] = tick
            event['number'] = machineNumber
            event['description'] = machineNumber + "/unload " + wipNumber
            simulation.AddEvent(event)

            wip.Checkin(simulation, shop, tick, leftCount)#把剩下的零件挪回在制品区

        else:#不插单
            self.asset['kickoff'] = tick
            if self.asset['index'] == self.GetBatch():
                self.asset['status'] = TaskStatus.RELEASE
                # print("release task")
                self.DoPrint()

    #更改任务状态
    def UpdateStatus(self, status, tick):
        if status == self.GetStatus():
            return
        self.asset['status'] = status
        
    # 输出任务状态
    def GetStatus(self):
        return self.asset['status']
    #输出最小经济批量 ，
    def GetBatch(self):
        return self.asset['batch']
    #设置最小经济批量
    def SetBatch(self, count):
        self.asset['batch'] = count
    #输出正在加工零件的序号
    def GetIndex(self):
        return self.asset['index']
    #输出已完成的零件数量
    def GetDoneCount(self):
        return self.asset['index']
    #输出零件所在机床编号
    def GetMachine(self):
        return self.asset['machine']

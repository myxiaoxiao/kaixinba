from MyShop import MyShop
from MyShop import ContextType
from MyTask import MyTask
from MyTask import TaskStatus
from MyTypes import Priority
from MyMachine import MachineStatus
from MyRule import MyRule
import random
import time

# 对生产模拟的目的就是，用模拟的方式相对精确的计算出在未来一段时间内是否能完成生产任务
# 如果模拟很多次的结果产生一个生态分布图，那么通过计算它的分布和置信区间来获得是否能完成生产任务的风险有多大

# 备忘录 2020-02-16
# 生产仿真主要包含3个方面的算法
# 1. 在制品库存按经济批量定义任务
# 2. 任务按优先级争取机床资源
# 3. 零件按其的任务批次序号进行更新，同时更新在制品库存的数量

# 备忘录 2020-02-18
# 明确基础数据中哪些是在动态变化的，哪些是静态不变
# 动态 : 最小经济批量表, 优先级表
# 但在制品的数量的更新有外部和内部两种情况（也属于动态数据）
# 外部情况：新的订单的到来会增加原材料数量, 从而更新在制品库存。外委回来的零件增加在制品数量
# 内部情况：按最小经济批量生产会减少在制品库存，完成的加工会增加在制品库存
# 动态节点和静态节点
# 动态节点
# 1. 局部更改最小经济批量元素
# 2. 局部更改优先级表元素
# 静态节点
# 1. 维护机床表, 工艺表,  在制品表, 机床的在制品对照表
# 2. 局部增加在制品数量
# 

# 备忘录 2020-02-18
# 整个仿真平台采用分布架构
# 仿真节点
#   在时间维度上，建立标准的模拟环境，用于模拟车间的零件生产过程。其中会涉及机床的状态变化、在制品向成品的流动变化、任务的开销
#   可以统计出生产过程中的所有动态数据，帮助人们更直观的分析和观察生产的过程
#   应用方向：
#       1. 帮助企业进行产能分析并做出决策
#       2. 人工智能学习提供样本数据
#       3. 智能工厂可视化仿真提供模拟数据输入源
# 动态节点
#   通过条件事件的形式驱动生产规则，从而影响在模拟过程中的数据的变化
#   v1.0 : 通过监控产能数据，来更改规则信息(直接开放python代码进行二次开发实现)
#   v2.0 : 通过open-api的形式，支持外部二次开发
#   v3.0 : 通过定义标准的事件驱动模型来更新规则
#
# 静态节点
#   维护模拟仿真所涉及的机床、工艺、在制品数量等相对稳定的资源型数据
#   v1.0 : 通过excel等数据表格定义资源数据
#   v2.0 : 开发工厂layout工具来摆放机床、在制品的位置和数量、工程师维护工艺的表单版本管理

# 算法备忘录 2020-02-29
# 改进计划 : 对于同一优先级维度的在制品或机床，可以随机轮选来保持一定的随机性，这样有助于搜索出最优结果


class MySim:
    def __init__(self):
        self.shop = MyShop()
        self.taskMap = {}
        self.rule = MyRule()
        self.tick = 0
        # minutes
        self.offlineData = {} # 在仿真的一步中产生的数据包(key:完成的任务编号，value：完成的任务数据(asset))
        self.priorityWips = [] #按优先级排序后的在制品列表   
        self.changing = True#是否更改 
        self.finishedMap = {}#成品零件编号(key),该零件数量(value)
        self.nextActiveTasks = None#下一步仿真实际要更新的任务
        self.idleMachines = None#空闲机床列表
        self.doRandom = True#是否打乱顺序
        self.events = []

    def AddEvent(self, event):
        self.events.append(event)

    def Change(self):#打乱顺序
        self.changing = True

    def GetRule(self):
        return self.rule
    def GetShop(self):
        return self.shop
    def GetOfflineData(self):#输出所有完成的任务
        return self.offlineData
    def GetOnlineData(self):#输出所有还在进行的任务
        onlineData = {}
        for taskNumber in self.taskMap:
            task = self.taskMap[taskNumber]
            onlineData[taskNumber] = task.ToData()
        return onlineData

    def GetEvents(self):
        return self.events

    def GetRunningData(self):#输出所有还在进行的任务
        onlineData = {}
        for taskNumber in self.taskMap:
            task = self.taskMap[taskNumber]

            runningData = {}
            runningData['machine'] = task.asset['machine']
            runningData['status'] = task.asset['status']
            wipNumber = task.asset['wip']
            wip = self.shop.GetObject(ContextType.WIP, wipNumber)
            runningData['pn'] = wip.asset['part']
            runningData['op'] = wip.asset['process']
            runningData['todo'] = task.asset['batch'] - task.asset['index']
            runningData['done'] = task.asset['index']

            onlineData[taskNumber] = runningData
        return onlineData

    def Initialize(self, setting):#初始化
        self.shop.Initialize(setting)
        self.rule.Initialize(setting)

    def UpdatePriorityWips(self):#将在制品按优先级排序
        priorityMap = {}
        wipMap = self.shop.GetContext(ContextType.WIP)
        priorityMap = {}
        for wipNumber in wipMap:
            wip = wipMap[wipNumber]
            part =  wip.GetPart()  
            priorityMap[wipNumber] = self.rule.GetPriority(part)
        self.priorityWips = sorted(priorityMap.items(), key=lambda x: x[1], reverse=False)

    def Run(self):
        self.doRandom = False
        start = time.time()
        while True:
            self.RunStep()
            if len(self.taskMap) == 0:
                break
        end = time.time()
        print("finish :" + str((end-start) * 1000))

    def RunStep(self):
        self.events.clear()
        # print(self.tick)
        if self.changing == True:
            self.UpdatePriorityWips()
            self.changing = False
        if len(self.priorityWips) == 0:
            # print("no priority")
            pass

        # 零件生产
        self.Production(self.tick)

        # 生产调度
        self.Scheduling(self.tick)
        
        nextCost = self.GetActiveTasks(self.tick)
        if len(self.taskMap) > 0:
            self.tick = self.tick + nextCost

    def GetLaunchWipsRandomly(self, machineNumber, ignoreWipNumber, priority):#输出能在该机床上加工的在制品（按优先级排序）
        wipNumbers = []
        for wipNumberPriority in self.priorityWips:
            wipNumber = wipNumberPriority[0]
            if wipNumber == ignoreWipNumber:
                continue
            wip = self.shop.GetObject(ContextType.WIP, wipNumber)
            quantity = wip.GetQuantity()
            if abs(quantity) < 0.0001:#排除掉全部加工完成的在制品
                continue

            isOn = self.shop.IsOnMachine(machineNumber, wipNumber)
            if isOn == False:#排除所有不能再该机床上加工的在制品
                continue

            wipPriority = wipNumberPriority[1]
            if priority != Priority.UNDEFINED and wipPriority != priority: #凡是不是指定的优先级全部排除掉
                continue

            wipNumbers.append(wipNumber)

        return wipNumbers

    def TryLauchHighPriorityTaskToMachine(self, tick, machine, priority, ignoreWipNumber):
        machineNumber = machine.GetNumber()
        launchWips = self.GetLaunchWipsRandomly(machineNumber, ignoreWipNumber, priority)#得到能在该机床上加工的在制品（按优先级排序）
        # 对于同一优先级维度的在制品，可以随机轮选来保持一定的随机性，这样有助于搜索出最优结果
        if priority != Priority.UNDEFINED:#判断是否指定了要加工在制品的优先级
            if self.doRandom:
                random.shuffle(launchWips)#打乱顺序
        else:
            # todo
            pass
        for wipNumber in launchWips:
            wip = self.shop.GetObject(ContextType.WIP, wipNumber)
            batch = self.rule.GetBatch(wipNumber)
            quantity = wip.GetQuantity()
            if quantity < batch:
                # 对于在制品如果达不到最小经济批量的搜索其前面的工序在制品数量，如果前面没需消化的在制品则不管忽略最小经济批量的限制
                process = self.shop.GetObject(ContextType.PROCESS, wip.GetProcess())
                if process.IsDispersed() == False:
                    continue

                has = self.HasComingFlow(wipNumber)
                if has == True:#该在制品之前是否还有和它相同类型的在制品在等待加工或者正在加工（看它是不是这个类型最后一个加工的在制品）
                    continue
                batch = quantity

            wip.Checkout(self, self.shop, tick, batch)
            task = MyTask(tick, wipNumber, machineNumber, batch)
            # event : 
            machine.Launch(self, tick, task.GetNumber())
            if priority == Priority.UNDEFINED:
                self.idleMachines.remove(machineNumber)#从空闲机床里删除该机床
            self.taskMap[task.GetNumber()] = task
            return True

        return False

    def Scheduling(self, tick):
        # 算法备忘录 2020-02-16
        # 过滤出状态为'就绪'的任务，建立(任务号,优先级)的对应表，并按优先级排序（优先级越高排在前面）
        # 过滤出状态为'空闲'的机床，按任务优先级给机床（该任务可以在该机床上加工和库存数量大于一次任务的批次数量）分配任务
        #   并启动该机床
        #   在制品库存更新

        # 算法备忘录 2020-02-17
        # 按优先级给机床分配在制品（替换现在的直接分配任务）
        # 由分配的在制品创建对应的任务

        machineMap = self.shop.GetContext(ContextType.MACHINE)
        
        if self.idleMachines == None:
            self.idleMachines = []#空闲机床列表
            for machineNumber in machineMap:
                machine = machineMap[machineNumber]
                if machine.GetStatus() != MachineStatus.IDLE:
                    continue
                self.idleMachines.append(machineNumber)
        
        # 对于同一优先级维度的机床，可以随机轮选来保持一定的随机性，这样有助于搜索出最优结果
        if self.doRandom == True:
            random.shuffle(self.idleMachines)

        index = 0
        while index < len(self.idleMachines):
            machineNumber = self.idleMachines[index]
            machine = machineMap[machineNumber]
            lanched = self.TryLauchHighPriorityTaskToMachine(tick, machine, Priority.UNDEFINED, None)
            if lanched == False:#如果没有任务分配给该机床，就去找下一个机床
                index = index + 1

    def Production(self, tick):
        # 算法备忘录 2020-02-16
        # 遍历任务表，更新每个任务的状态（KICKOFF，SETUP，RUNNING，TEARDOWN，DONE）
        #   当一个任务里可以包含多个零件的加工，第一个零件的加工时间包含了setup时间，后续的零件可以重用第一个零件的装夹
        #   当一个零件完成加工，任务的下一个零件自动进入开始状态(KICKOFF)
        #   当任务的所有零件都加工完成，这个任务的状态为Release
        # 卸载任务表中已经完成的任务

        # 算法备忘录 2020-02-22
        # 当一个任务的完成的时候, 如果该任务对应的工艺是可离散的且它的优先级不是高优先级，那么高优先级的任务可进行插单操作
        #   暂停当前任务的批次的后续零件的加工
        #   机床资源分配给高优先级的任务

        self.offlineData.clear()
        if self.nextActiveTasks == None:
            self.nextActiveTasks = []
            for taskNumber in self.taskMap:
                self.nextActiveTasks.append(taskNumber)
        for taskNumber in self.nextActiveTasks:
            task = self.taskMap[taskNumber]
            wipNumber = task.GetWip()
            wip = self.shop.GetObject(ContextType.WIP, wipNumber)
            taskProcessNumber = wip.GetProcess()
            taskProcess = self.shop.GetObject(ContextType.PROCESS, taskProcessNumber)
            setup = taskProcess.GetSetup()
            duration = taskProcess.GetDuration()
            teardown = taskProcess.GetTeardown()
            if task.GetIndex() > 0:
                setup = 0

            passed = tick - task.GetKickoff()
            if passed >= setup + duration + teardown:
                # event : 
                machineNumber = task.GetMachine()
                machine = self.shop.GetObject(ContextType.MACHINE, machineNumber)
                part = wip.GetPart()
                priority = self.rule.GetPriority(part)
                inserted = False
                if priority == Priority.HIGH:
                    task.FinishPart(self, tick, self.shop, False)
                else:
                    process = self.shop.GetObject(ContextType.PROCESS, wip.GetProcess())
                    if process.IsDispersed() == True:
                        inserted = self.TryLauchHighPriorityTaskToMachine(tick, machine, Priority.HIGH, wip.GetNumber())
                        task.FinishPart(self, tick, self.shop, inserted)
                    else:
                        task.FinishPart(self, tick, self.shop, False)
                if task.GetStatus() == TaskStatus.RELEASE:
                    if inserted == False:
                        machine.SetStatus(tick, MachineStatus.IDLE)
                        self.idleMachines.append(machineNumber)

                        event = {}
                        event['location'] = 'machine'
                        event['time'] = tick
                        event['number'] = machineNumber
                        event['description'] = machineNumber + "/idle"
                        self.AddEvent(event)

                    self.offlineData[taskNumber] = task.ToData()
                    nextProcess = wip.GetNextProcess(self.shop)
                    if nextProcess == None:
                        if part not in self.finishedMap:
                            self.finishedMap[part] = 0
                         # event : 
                        self.finishedMap[part] = self.finishedMap[part] + task.GetDoneCount()

                        event = {}
                        event['location'] = 'finish'
                        event['time'] = tick
                        event['number'] = part
                        event['description'] = part + "/append " + str(task.GetDoneCount()) + " -> " + str(self.finishedMap[part])
                        self.AddEvent(event)

                    del self.taskMap[taskNumber]

            # teardown
            elif passed >= setup + duration:
                 # event : 
                task.UpdateStatus(TaskStatus.TEARDOWN, tick)

                machineNumber = task.GetMachine()
                event = {}
                event['location'] = 'machine'
                event['time'] = tick
                event['number'] = machineNumber
                event['description'] = machineNumber + "/teardown " + wipNumber
                self.AddEvent(event)


            # running
            elif passed >= setup:
                 # event : 
                task.UpdateStatus(TaskStatus.RUNNING, tick)

                machineNumber = task.GetMachine()
                event = {}
                event['location'] = 'machine'
                event['time'] = tick
                event['number'] = machineNumber
                event['description'] = machineNumber + "/running " + wipNumber
                self.AddEvent(event)


            # setup
            else:
                 # event : 
                task.UpdateStatus(TaskStatus.SETUP, tick)

                machineNumber = task.GetMachine()
                event = {}
                event['location'] = 'machine'
                event['time'] = tick
                event['number'] = machineNumber
                event['description'] = machineNumber + "/setup " + wipNumber
                self.AddEvent(event)


    def HasComingFlow(self, wipNumber):#看该在制品之前是否还有和它相同类型的在制品在等待加工或者正在加工（看它是不是这个类型最后一个加工的在制品）
        has = self.shop.HasWipComingFlow(wipNumber)
        if has == True:
            return True
        else:
            wip = self.shop.GetObject(ContextType.WIP, wipNumber)
            processNumber = wip.GetProcess()
            process = self.shop.GetObject(ContextType.PROCESS, processNumber)
            processIndex = process.GetIndex()
            part = wip.GetPart()

            for taskNumber in self.taskMap:
                task = self.taskMap[taskNumber]
                taskWipNumber = task.GetWip()
                taskWip = self.shop.GetObject(ContextType.WIP, taskWipNumber)
                taskPart = taskWip.GetPart()
                if taskPart != part:#过滤不是指定的在制品
                    continue

                taskProcessNumber = taskWip.GetProcess()
                taskProcess = self.shop.GetObject(ContextType.PROCESS, taskProcessNumber)
                taskProcessIndex = taskProcess.GetIndex()
                if taskProcessIndex < processIndex:
                    if taskProcess.IsDispersed() == True:
                        return True
                    else:
                        continue

            return False
    
    def GetFinishedMap(self):
        return self.finishedMap

    def GetActiveTasks(self, tick):
        self.nextActiveTasks = []
        # 遍历所有的任务
        minCost = 1000000
        for taskNumber in self.taskMap:
            task = self.taskMap[taskNumber]
            kickoff = task.GetKickoff()
            wipNumber = task.GetWip()
            wip = self.shop.GetObject(ContextType.WIP, wipNumber)
            taskProcessNumber = wip.GetProcess()
            taskProcess = self.shop.GetObject(ContextType.PROCESS, taskProcessNumber)
            setup = taskProcess.GetSetup()
            duration = taskProcess.GetDuration()
            teardown = taskProcess.GetTeardown()
            status = task.GetStatus()
            if task.GetIndex() > 0:
                setup = 0

            nextCost = 1000000
            if status == TaskStatus.SETUP:
                nextCost  = kickoff + setup - tick
            elif status == TaskStatus.RUNNING:
                nextCost = kickoff + setup + duration - tick
            elif status == TaskStatus.TEARDOWN:
                nextCost = kickoff + setup + duration + teardown - tick
            else:
                pass
        
            if nextCost < minCost:
                minCost = nextCost
                self.nextActiveTasks.clear()
                self.nextActiveTasks.append(taskNumber)
            elif abs(nextCost - minCost) < 0.00001:
                self.nextActiveTasks.append(taskNumber)
        
        return minCost
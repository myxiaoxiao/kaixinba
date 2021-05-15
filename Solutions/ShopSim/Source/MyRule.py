from MyShop import ContextType

# 备忘录 2020-02-16 (1)
# 维护在制品库存的最新经济批量
# 一般情况下，最小经济批量是个常量，主要是让生产准备以一个合理的零件数量进行准备和减少每次装夹定位的时间
# 但是特殊情况，由于在制品的数量始终无法达到固定的最小经济批量，导致该零件始终得到生产反而会延误该零件的交付
#   统计每个在制品库存的转化产能，对于产能低于计划产能的在制品，可以降低最小经济批量来增大转化率从而提高产能
#       一个标准批次会被分割成多个更小经济批量的批次在多台设备上同时进行加工

# 备忘录 2020-02-16 (2)
# 在最小经济批量保持不变的情况下
# 在生产过程中有三种层次的优先级
# 高优先级：优先分配此任务给机床，可强制暂停其他任务的后续批次零件的加工，进行进行插单生产
# 中优先级：优先分配此任务给机床
# 低优先级：按机床空闲分任务给机床

# 备忘录 2020-02-16 (3)
# 在模拟中可以通过随机更改（高优先级任务）经济批量来模拟人为应急调度

# 备忘录 2020-02-18
# 最新经济批量表在仿真过程可以动态更改
# 优先级表在仿真过程中可以动态更改

class MyRule():
    def __init__(self):
        # wip-batch : 最小经济批量表
        self.batchDynamicMap = {}
        # part-priority : 优先级表
        self.priorityDynamicMap = {}
    #更改最小经济批量
    def ChangeBatch(self, wip, batch):
        self.batchDynamicMap[wip] = batch
    #更改优先级表
    def ChangePriority(self, partNumber, priority):
        self.priorityDynamicMap[partNumber] = priority
    #输出最小经济批量
    def GetBatch(self, wipNumber):
        if wipNumber not in self.batchDynamicMap:
            return None
        return self.batchDynamicMap[wipNumber]
    #输出优先级表
    def GetPriority(self, partName):
        if partName not in self.priorityDynamicMap:
            return None
        return self.priorityDynamicMap[partName]
    #初始化表格
    def Initialize(self, setting):
        self.InitializeBatchMap(setting)
        self.InitializePriorityMap(setting)
    #初始化最小经济批量表格
    def InitializeBatchMap(self, setting):
        # 备忘录 2020-02-17
        # 读配置信息创建batch map
        if 'batchs' in setting:
            batchs = setting['batchs']
            for it in batchs:
                wipNumber = it['number']
                batchSize = it['size']
                self.batchDynamicMap[wipNumber] = int(batchSize)
    #初始化优先级表格
    def InitializePriorityMap(self, setting):
        pass
        # 备忘录 2020-02-17
        # 读配置信息创建priority map
        if 'priorities' in setting:
            priorities = setting['priorities']
            for it in priorities:
                wipNumber = it['number']
                proprity = int(it['priority'])
                self.priorityDynamicMap[wipNumber] = proprity

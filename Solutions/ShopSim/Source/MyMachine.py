from MyData import MyData
from MyTypes import MachineStatus

class MyMachine(MyData):
    def __init__(self, number):
        MyData.__init__(self)
        self.SetNumber(number) # 机床编号
        self.asset['status'] = MachineStatus.IDLE #状态
        self.asset['task'] = '' # 任务
        self.timeline = []

    # 获取机床的状态
    def GetStatus(self):
        return self.asset['status']
    # 更改机床状态
    def SetStatus(self, tick, status):
        if MachineStatus.IDLE == status or MachineStatus.PLANSTOP == status: 
            self.Append(tick, None)
        else:
            self.Append(tick, self.asset['task'])
        self.asset['status'] = status

    # 加载任务
    def Launch(self, simulation, tick, taskNumber):
        self.asset['task'] = taskNumber
        self.SetStatus(tick, MachineStatus.RUNNING)
        # print("machine launch")
        event = {}
        event['location'] = 'machine'
        event['time'] = tick
        event['number'] = self.asset['number']
        event['description'] = self.asset['number'] + "/load " + taskNumber
        simulation.AddEvent(event)
        self.DoPrint()

    def Append(self, tick, taskNumber):
        item = {}
        item['tick'] = tick
        item['taskNumber'] = taskNumber
        self.timeline.append(item)
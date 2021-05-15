#对象类型
class ContextType:
    MACHINE = 0 #机床类
    PROCESS = 1 #工艺类
    WIP = 2 #在制品类
#机床状态
class MachineStatus:
    IDLE = 1 #空闲
    RUNNING = 2 #运行
    PLANSTOP = 3 #因机床维修，等其他特殊情况而停机，导致工作暂停
#优先级
class Priority:
    UNDEFINED = 0 #未定义
    HIGH = 1 #高
    MIDDLE = 2 #中
    LOW = 3 #低
#任务状态
class TaskStatus:#（按批次加工）
    SETUP = 1 #装夹
    RUNNING = 2 #正在加工
    TEARDOWN = 3 #拆卸
    RELEASE = 4 #全批的零件做完(注：当批次加工被打断时，直接算任务完成（进入RELEASE状态)
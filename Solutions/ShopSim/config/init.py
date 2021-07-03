import requests
import time
import json
import xlrd

serviceIp = "http://127.0.0.1:21560"
USER = "test"

def GetTableData(table):
    items = []
    rowsCount = table.nrows
    columnCount = table.ncols
    for rowIndex in range(rowsCount):
        if rowIndex == 0:
            continue
        item = []
        for columnIndex in range(columnCount):
            item.append(table.cell(rowIndex,columnIndex).value)
        items.append(item)
    
    return items

def IsTrue(value):
    if abs(value - 1) < 0.0001:
        return True
    else:
        return False

def IsZero(value):
    if abs(value - 0) < 0.0001:
        return True
    else:
        return False

def Initialize(excelFile):
    data = xlrd.open_workbook(excelFile)
    print("sheets：" + str(data.sheet_names()))

    setting = {}

    # machine table
    table = data.sheet_by_name('machine')
    items = GetTableData(table)
    machines = []
    for item in items:
        machine = {}
        machine['number'] = item[0]
        machines.append(machine)
    setting['machines'] = machines

    # process table
    table = data.sheet_by_name('process')
    items = GetTableData(table)
    processes = []
    for item in items:
        process = {}
        partName = item[0]
        process['wip'] = partName + '_' + item[1]
        process['number'] = partName + '_' + item[2]
        process['setup'] = item[3]
        process['duration'] = item[4]
        process['teardown'] = item[5]
        process['next'] = partName + '_' + item[6]
        process['dispersed'] = True
        processes.append(process)
    table = data.sheet_by_name('map')
    items = GetTableData(table)
    procesMachineMap = {}
    for item in items:
        part = item[0]
        processNumber = part + "_" + item[1]
        procesMachineMap[processNumber] = {}
        for j in range(2,len(item)):
            if IsZero(item[j]) == True:
                continue
            machineNumber = machines[j-2]['number']
            procesMachineMap[processNumber][machineNumber] = item[j]
    for process in processes:
        processNumber = process['number']
        process['machineCapacityMap'] = procesMachineMap[processNumber]
    setting['processes'] = processes

    # wip table
    table = data.sheet_by_name('wip')
    items = GetTableData(table)
    wips = []
    for item in items:
        wip = {}
        wip['part'] = item[0]
        wip['number'] = item[0] + "_" + item[1]
        wip['quantity'] = item[2]
        wips.append(wip)
    setting['wips'] = wips

    # batch table
    table = data.sheet_by_name('batch')
    items = GetTableData(table)
    bacths = []
    for item in items:
        bacth = {}
        part = item[0]
        bacth['number'] = part + "_" + item[1]
        bacth['size'] = item[2]
        bacths.append(bacth)
    setting['batchs'] = bacths

    # priority table
    table = data.sheet_by_name('priority')
    items = GetTableData(table)
    priorities = []
    for item in items:
        priority = {}
        priority['number'] = item[0]
        priority['priority'] = item[1]
        priorities.append(priority)
    setting['priorities'] = priorities
    return setting

def Post(package, url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    value = json.dumps(package).encode()
    response = requests.post(serviceIp + url, data = value, headers = headers)
    text = response.content.decode()
    content = json.loads(text)
    return content

def Connect(setting):
    data = {}
    data["user"] = USER
    data['setting'] = setting
    return Post(data, '/Connect')

def Run():
    data = {}
    data["user"] = USER
    return Post(data, '/Run')

if __name__ == '__main__':

    # setting = Initialize('setting_big.xlsx')
    setting = Initialize('shop_config.xlsx')
    Connect(setting)

    # Run()

    exit(0)
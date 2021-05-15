import abc

class MyData:
    def __init__(self):
        self.asset = {}
        self.asset['number'] = ''
    
    def GetNumber(self):
        return self.asset['number']

    def SetNumber(self, number):
        self.asset['number'] = number

    def ToData(self):
        return self.asset

    def DoPrint(self):
        pass
        # for it in self.asset:
        #     print(str(it) + " : " + str(self.asset[it]))
        # print('-------------------------------------------')


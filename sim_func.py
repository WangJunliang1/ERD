
from collections import OrderedDict

# resPack = ResPack()
# resPack.addCell("t1", "20", 123)
# resPack.addCell("t1", "40", 234)
# resPack.addCell("t1", "60", 567)
# resPack.addCell("t2", "20", 323)
# resPack.addCell("t2", "40", 423)
# resPack.addCell("t2", "60", 523)
# print(resPack.getCellCount())
# print(resPack.getCellNameList())
# print(resPack.getCellValue("t2", "40"))
# print(resPack.getCellValue("t1", "60"))
# print(resPack.getCellValue("t1", "50"))
# print(resPack.getCellFlagList("t1"))
# print(resPack.getCellFlagListByIndex(1))
# print(resPack.getCellFlagCount("t2"))
# print(resPack.getCellFlagCountByIndex(0))


class ResData:
    def __init__(self):
        self.bandwidth = 0
        self.latency = 0

    def setBandWidth(self, bandwidth):
        self.bandwidth = bandwidth

    def getBandWidth(self):
        return self.bandwidth

    def setValue(self, latency):
        self.latency = latency

    def getValue(self):
        return self.latency


class ResCell:
    def __init__(self):
        self.name = ""
        self.valMap = OrderedDict()

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getFlagList(self):
        flagList = []
        for key, _ in sorted(self.valMap.items()):
            flagList.append(key)
        return flagList

    def setData(self, flag, bandwidth, value):
        if not flag in self.valMap:
            self.valMap[flag] = ResData()
        self.valMap[flag].setValue(value)
        self.valMap[flag].setBandWidth(bandwidth)

    def getDataCount(self):
        return len(self.valMap)

    def getData(self, flag):
        if flag in self.valMap:
            return self.valMap[flag].getBandWidth(), self.valMap[flag].getValue()
        else:
            return None, None


class ResPack:
    def __init__(self):
        self.resCellList = []

    def getCellCount(self):
        return len(self.resCellList)

    def addCell(self, name, flag, bandwidth, value):
        for resCell in self.resCellList:
            if resCell.getName() == name:
                resCell.setData(flag, bandwidth, value)
                return
        resCell = ResCell()
        resCell.setName(name)
        resCell.setData(flag, bandwidth, value)
        self.resCellList.append(resCell)

    def getCellNameList(self):
        nameList = []
        for resCell in self.resCellList:
            nameList.append(resCell.getName())
        return nameList

    def getCellNameByIndex(self, index):
        return self.resCellList[index].getName()

    def getCellFlagCount(self, name):
        for resCell in self.resCellList:
            if resCell.getName() == name:
                return resCell.getDataCount()
        return None

    def getCellFlagCountByIndex(self, index):
        return self.resCellList[index].getDataCount()

    def getCellFlagList(self, name):
        for resCell in self.resCellList:
            if resCell.getName() == name:
                return resCell.getFlagList()
        return None

    def getCellFlagListByIndex(self, index):
        return self.resCellList[index].getFlagList()

    def getCellData(self, name, flag):
        for resCell in self.resCellList:
            if resCell.getName() == name:
                return resCell.getData(flag)
        return None, None

import os

def _(text):
    return text

class menuManager():
    def __init__(self):
        self.menu = {}
        self.currIndex = None
    def loadMenuByPath(self, path, reset = True):
        self.loadMenuByPathList([path], reset)
    def loadMenuByPathList(self, pathList, reset = True):
        menuDict = {}
        for path in pathList:
            menuDict = self.FsTreeToDict(path, baseMenuDict = None)
        self.loadMenuByDict(menuDict, reset)
    def loadMenuByDict(self, menuDict, reset = True):
        self.menu = menuDict.copy()
        if reset:
            self.resetMenu()
        else:
            self.restoreMenu()
    def resetMenu(self):
        self.currIndex = None
        if len(self.getMenuDict()) > 0:
            self.currIndex = [0]
    def restoreMenu(self):
        if self.currIndex != None:
            try:
                r = self.getValueByPath(self.menu, self.currIndex)
                if r == {}:
                    self.currIndex = None
            except:
                self.currIndex = None
    def nextEntry(self):
        if self.currIndex == None:
            return False
        if self.currIndex[len(self.currIndex) - 1] + 1 >= len(self.getNestedByPath(self.getMenuDict(), self.currIndex[:-1])):
           self.currIndex[len(self.currIndex) - 1] = 0 
        else:
            self.currIndex[len(self.currIndex) - 1] += 1
        return True
    def firstEntry(self):
        if self.currIndex == None:
            return False
        self.currIndex[len(self.currIndex) - 1] = 0
    def lastEntry(self):
        if self.currIndex == None:
            return False
        self.currIndex[len(self.currIndex) - 1] = len(self.getNestedByPath(self.getMenuDict(), self.currIndex[:-1]))
    def prevEntry(self):
        if self.currIndex == None:
            return False
        if self.currIndex[len(self.currIndex) - 1] == 0:
           self.currIndex[len(self.currIndex) - 1] = len(self.getNestedByPath(self.getMenuDict(), self.currIndex[:-1])) - 1
        else:
            self.currIndex[len(self.currIndex) - 1] -= 1
        return True

    def enterMenu(self):
        if self.currIndex == None:
            return False
        try:
            r = self.getValueByPath(self.getMenuDict(), self.currIndex + [0])
            if r == {}:
                return False
        except:
            return False
        self.currIndex.append(0)
        return True
    def leaveMenu(self):
        if self.currIndex == None:
            return False
        if len(self.currIndex) == 1:
            return False
        self.currIndex = self.currIndex[:len(self.currIndex) - 1]
        return True
    def activateCurrentEntry(self):
        if self.currIndex == None:
            return
    def getMenuDict(self):
        return self.menu
    def printMenu(self):
        self.printDict(self.getMenuDict())
    def printDict(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.printDict(value, indent + 1)

    def FsTreeToDict(self, path, baseMenuDict = None):
        if isinstance(baseMenuDict, dict):
            menuDict = baseMenuDict
        else:
            menuDict = {}
        for root, dirs, files in os.walk(path):
            for d in dirs:
                try:
                    if d.startswith('__'):
                        continue
                    menuDict.update({d + ' ' + _('Menu'): self.FsTreeToDict(os.path.join(root, d)) })
                except Exception as e:
                    print(e)
            for f in files:
                try:
                    fileName, fileExtension = os.path.splitext(f)
                    fileName = fileName.split('/')[-1]
                    if fileName.startswith('__'):
                        continue
                    command = fileName + ' ' + _('Action') + ' Command'
                    menuDict.update({fileName + ' ' + _('Action'): command})
                except Exception as e:
                    print(e)
            return menuDict  # note we discontinue iteration trough os.walk

    def getCurrIndex(self):
        if self.currIndex == None:
            return 0        
        return self.currIndex[len(self.currIndex) - 1]

    def getCurrentValue(self):
        return self.getValueByPath(self.getMenuDict(), self.currIndex)

    def getCurrentKey(self):
        return self.getKeysByPath(self.getMenuDict(), self.currIndex)[self.currIndex[-1]]

    def getNestedByPath(self, complete, path):
        path = path.copy()
        if path != []:
            index = list(complete.keys())[path[0]]
            nested = self.getNestedByPath(complete[index], path[1:])
            return nested
        else:
            return complete

    def getKeysByPath(self, complete, path):
        if not isinstance(complete, dict):
            return []
        d = complete
        for i in path[:-1]:
            d = d[list(d.keys())[i]]
        return list(d.keys())

    def getValueByPath(self, complete, path):
        if not isinstance(complete, dict):
            return complete
        d = complete.copy()
        for i in path:
            d = d[list(d.keys())[i]]
        return d

m = menuManager()
m.loadMenuByPath('/home/chrys/Projekte/dragonFM/src/dragonfilemanager/commands/detail-menu/')
m.printMenu()
print(m.getCurrentValue())
m.nextEntry()
print(m.getCurrentValue())
m.enterMenu()
print(m.getCurrentValue())
print(m.getCurrentKey())


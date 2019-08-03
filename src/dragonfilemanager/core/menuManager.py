import os

def _(text):
    return text
def loadFolderFunction(text):
    return text + ' ' + _('Menu')
def loadFileFunction(text):
    return text + ' ' + _('Action')

class menuManager():
    def __init__(self, menu = None, fileFunction = loadFileFunction, folderFunction = loadFolderFunction):
        self.menu = {}
        self.currIndex = None
        self.loadFolderFunction = folderFunction
        self.loadFileFunction = fileFunction
        if menu != None:
            if isinstance(menu, str):
                self.loadMenuByPath(menu)
            elif isinstance(menu, list):
                self.loadMenuByPathList(menu)
            elif isinstance(menu, dict):
                self.loadMenuByDict(menu)
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
    def setLoadFolderFunction(self, func):
        self.loadFolderFunction = func
    def setLoadFileFunction(self, func):
        self.loadFileFunction = func
    def getLoadFolderFunction(self):
        return self.loadFolderFunction
    def getLoadFileFunction(self):
        return self.loadFileFunction
    def getCurrentMenuSize(self):
        return len(self.getNestedByPath(self.getMenuDict(), self.currIndex[:-1]))
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
        if self.currIndex[len(self.currIndex) - 1] + 1 >= self.getCurrentMenuSize():
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
        self.currIndex[len(self.currIndex) - 1] = self.getCurrentMenuSize() - 1
    def prevEntry(self):
        if self.currIndex == None:
            return False
        if self.currIndex[len(self.currIndex) - 1] == 0:
           self.currIndex[len(self.currIndex) - 1] = self.getCurrentMenuSize() - 1
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
                    entryName = self.getLoadFolderFunction()(d)
                    menuDict.update({entryName: self.FsTreeToDict(os.path.join(root, d)) })
                except Exception as e:
                    print(e)
            for f in files:
                try:
                    fileName, fileExtension = os.path.splitext(f)
                    fileName = fileName.split('/')[-1]
                    if fileName.startswith('__'):
                        continue
                    command = self.getLoadFileFunction()(root+'/'+f)
                    menuDict.update({fileName + ' ' + _('Action'): command})
                except Exception as e:
                    print(e)
            return menuDict  # note we discontinue iteration trough os.walk

    def getIndexCurrLevel(self):
        if self.currIndex == None:
            return False
        return self.currIndex[len(self.currIndex) - 1]

    def getCurrentEntry(self):
        if self.currIndex == None:
            return False
        entry = self.getValueByPath(self.getMenuDict(), self.currIndex)
        if isinstance(entry, dict):
            entry = self.getCurrentKey()
        return entry

    def getEntryForIndexCurrLevel(self, index):
        if self.currIndex == None:
            return False
        entry = self.getValueByPath(self.getMenuDict(), self.currIndex[:-1] + [index])
        if isinstance(entry, dict):
            entry = self.getKeyOnIndex(index)
        return entry

    def getCurrentKey(self):
        if self.currIndex == None:
            return False
        return self.getKeyOnIndex(self.currIndex[-1])

    def getKeyOnIndex(self, index):
        if self.currIndex == None:
            return False
        return self.getKeysByPath(self.getMenuDict(), self.currIndex)[index]
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
'''

m = menuManager()
m.loadMenuByPath('/home/chrys/Projekte/dragonFM/src/dragonfilemanager/commands/detail-menu/')
m.printMenu()
print('')
print(m.getCurrentEntry())
print('')
print(m.getEntryForIndexCurrLevel(1))
m.nextEntry()
print(m.getCurrentEntry())
m.enterMenu()
print(m.getCurrentEntry())
print(m.getCurrentKey())
'''

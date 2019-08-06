import os, time

def _(text):
    return text

def getName(fullPath, text):
    return os.path.basename(fullPath)

def getVisible(fullPath, entry):
    return True

class menuManager():
    def __init__(self, menu = None, loadFileFunction = _, loadFolderFunction = _, loadFolderNameFunction = getName, loadFileNameFunction = getName, loadFolderVisibleFunction = getVisible, loadFileVisibleFunction = getVisible):
        self.menu = []
        self.currIndex = None
        self.typeAheadSearch = ''
        self.lastTypeAheadTime = time.time()
        self.loadFolderFunction = loadFolderFunction
        self.loadFileFunction = loadFileFunction
        self.loadFolderNameFunction = loadFolderNameFunction
        self.loadFileNameFunction = loadFileNameFunction
        self.loadFolderVisibleFunction = loadFolderVisibleFunction
        self.loadFileVisibleFunction = loadFileVisibleFunction
        if menu != None:
            if isinstance(menu, str):
                self.loadMenuByPath(menu)
            elif isinstance(menu, list):
                self.loadMenuByPathList(menu)
    def loadMenuByPath(self, path, reset = True):
        self.loadMenuByPathList([path], reset)
    def loadMenuByPathList(self, pathList, reset = True):
        menu = {}
        for path in pathList:
            menu = self.FsTreeToMenu(path, baseMenu = [])
        self.loadMenuByValue(menu, reset)
    def loadMenuByValue(self, menu, reset = True):
        self.menu = menu.copy()
        if reset:
            self.resetMenu()
        else:
            self.restoreMenu()

    def setLoadFolderFunction(self, func):
        self.loadFolderFunction = func
    def setLoadFileFunction(self, func):
        self.loadFileFunction = func
    def setLoadFolderNameFunction(self, func):
        self.loadFolderNameFunction = func
    def setLoadFileNameFunction(self, func):
        self.loadFileNameFunction = func
    def setLoadFolderVisibleFunction(self, func):
        self.loadFolderVisibleFunction = func
    def setLoadFileVisibleFunction(self, func):
        self.loadFileVisibleFunction = func

    def getLoadFolderFunction(self):
        return self.loadFolderFunction
    def getLoadFileFunction(self):
        return self.loadFileFunction
    def getLoadFolderNameFunction(self):
        return self.loadFolderNameFunction
    def getLoadFileNameFunction(self):
        return self.loadFileNameFunction
    def getLoadFolderVisibleFunction(self):
        return self.loadFolderVisibleFunction
    def getLoadFileVisibleFunction(self):
        return self.loadFileVisibleFunction
    # type ahead
    def resetTypeAheadSearch(self, force = False):
        if (time.time() - self.lastTypeAheadTime > 1.5) or force:
            self.typeAheadSearch = ''
    def doTypeAheadSearch(self, key):
        # useful for type ahead search?
        if self.currIndex == None:
            return False
        if key == None:
            return False
        if not isinstance(key, str):
            return False
        if len(key) != 1:
            return False
        key = key.lower()
        if not key in '.-_0123456789abcdefghijklmnopqrstuvwxyz':
            return False
        menuLen = self.getCurrentMenuSize()
        if menuLen < 2:
            return False
        # then search
        if self.typeAheadSearch != key:
            self.typeAheadSearch += key

        startIndex = self.getIndexCurrLevel()
        searchIndex = startIndex

        searchString = '{0}'.format(self.typeAheadSearch)
        while True:
            if len(self.typeAheadSearch) == 1:
                # jump always to next match if only one first letter nav (==1)
                searchIndex += 1
                if searchIndex >= menuLen:
                    searchIndex = 0
                if searchIndex == startIndex:
                    return False
            # search by name column
            entry = self.getEntryForIndexCurrLevel(searchIndex)
            if entry['name'].lower().startswith(searchString):
                self.currIndex[len(self.currIndex) - 1] = searchIndex
                self.lastTypeAheadTime = time.time()
                return True
            elif len(self.typeAheadSearch) > 1:
                # keep current match until its not matching 
                # anymore for type ahead search (> 1)
                searchIndex += 1
                if searchIndex >= menuLen:
                    searchIndex = 0
                if searchIndex == startIndex:
                    return False
    def resetTypeAheadSearch(self, force = False):
        if (time.time() - self.lastTypeAheadTime > 1.5) or force:
            self.typeAheadSearch = ''

    def getCurrentMenuSize(self):
        d = self.getMenu().copy()
        path = self.currIndex
        currLen = 0
        # unpack
        for i in path:
            if isinstance(d, dict):
                currLen = len(d['value'])
                d = d['value'][list(d['value'].keys())[i]]
            elif isinstance(d, list):
                currLen = len(d)
                d = d[i]
        return currLen
    def resetMenu(self):
        self.currIndex = None
        if len(self.getMenu()) > 0:
            self.currIndex = [0]
    def setIndexCurrLevel(self, index):
        self.currIndex[len(self.currIndex) - 1] = index
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
        if self.getIndexCurrLevel() + 1 >= self.getCurrentMenuSize():
           self.firstEntry()
        else:
            self.setIndexCurrLevel( self.getIndexCurrLevel() + 1)
        return True
    def firstEntry(self):
        if self.currIndex == None:
            return False
        self.setIndexCurrLevel(0)
        return True

    def lastEntry(self):
        if self.currIndex == None:
            return False
        self.setIndexCurrLevel(self.getCurrentMenuSize() - 1)
        return True

    def prevEntry(self):
        if self.currIndex == None:
            return False
        if self.getIndexCurrLevel() == 0:
           self.lastEntry()
        else:
            self.setIndexCurrLevel( self.getIndexCurrLevel() - 1)
        return True

    def enterMenu(self):
        if self.currIndex == None:
            return False
        try:
            r = self.getValueByPath(self.getMenu(), self.currIndex + [0])
            if r == {}:
                return False
        except Exception as e:
            print(e)
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
    def getMenu(self):
        return self.menu
    def printMenu(self):
        for e in self.getMenu():
            self.printMenuEntry(e)
    def printMenuEntry(self, d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print('\t' * indent + str(key))
                self.printMenuEntry(value, indent + 1)
            else:
                print('\t' * indent + str(key) + ': ' + str(value))

    def FsTreeToMenu(self, path, baseMenu = None):
        if isinstance(baseMenu, list):
            menu = baseMenu
        else:
            menu = {}
        for root, dirs, files in os.walk(path):
            for d in dirs:
                try:
                    if d.startswith('__'):
                        continue
                    fullPath = os.path.join(root, d)
                    entry = self.createMenuEntry(fullPath)
                    if isinstance(menu, dict):
                        menu.update({d: entry})
                    elif isinstance(menu, list):
                        menu.append(entry)
                except Exception as e:
                    print(e)
            for f in files:
                try:
                    fileName, fileExtension = os.path.splitext(f)
                    fileName = fileName.split('/')[-1]
                    if fileName.startswith('__'):
                        continue
                    fullPath = os.path.join(root, f)
                    entry = self.createActionEntry(fullPath)
                    if isinstance(menu, dict):
                        menu.update({fileName: entry})
                    elif isinstance(menu, list):
                        menu.append(entry)
                except Exception as e:
                    print(e)
            return menu  # note we discontinue iteration trough os.walk
    def createActionEntry(self, fullPath):
        entryValue = self.getLoadFileFunction()(fullPath)
        return {
            'fullPath': fullPath,
            'type':  'action',
            'name': self.getLoadFileNameFunction()(fullPath, entryValue),
            'value': entryValue,
            'visible': self.getLoadFileVisibleFunction()(fullPath, entryValue)
        }
    def createMenuEntry(self, fullPath):
        entryMenuValue = self.FsTreeToMenu(fullPath)
        return {
            'fullPath': fullPath,
            'type':  'menu',
            'name': self.getLoadFolderNameFunction()(fullPath, entryMenuValue),
            'value': entryMenuValue,
            'visible': self.getLoadFolderVisibleFunction()(fullPath, entryMenuValue)
        }
    def getIndexCurrLevel(self):
        if self.currIndex == None:
            return False
        return self.currIndex[len(self.currIndex) - 1]

    def getCurrentEntry(self):
        if self.currIndex == None:
            return False
        entry = self.getValueByPath(self.getMenu(), self.currIndex)
        return entry

    def getEntryForIndexCurrLevel(self, index):
        if self.currIndex == None:
            return False
        entry = self.getValueByPath(self.getMenu(), self.currIndex[:-1] + [index])
        return entry

    def getNestedByPath(self, complete, path):
        path = path.copy()
        if path != []:
            index = 0
            if isinstance(complete, dict):
                if complete['type'] == 'menu':
                    index = list(complete.keys())[path[0]]
                elif complete['type'] == 'action':
                    index = complete[list(complete.keys())[i]]
            elif isinstance(complete, list):
                index = path[0]
            nested = self.getNestedByPath(complete[index], path[1:])
            return nested
        else:
            return complete

    def getValueByPath(self, complete, path):
        if isinstance(complete, dict):
            if complete['type'] == 'action':
                return complete
        d = complete.copy()
        for i in path:
            if isinstance(d, dict):
                if d['type'] == 'menu':
                    d = d['value'][list(d['value'].keys())[i]]
                elif d['type'] == 'action':
                    d = d[list(d.keys())[i]]
            elif isinstance(d, list):
                d = d[i]
        return d

'''
m = menuManager()
m.loadMenuByPath('/home/chrys/Projekte/dragonFM/src/dragonfilemanager/commands/detail-menu/')
m.printMenu()

print(m.getCurrentEntry()['name'])
m.nextEntry()
print(m.getCurrentEntry()['name'])
print(2,m.getCurrentMenuSize())
m.enterMenu()
print(m.getCurrentEntry()['name'])
m.nextEntry()
print(m.getCurrentEntry()['name'])
m.nextEntry()
print(m.getCurrentEntry()['name'])
m.nextEntry()
print(m.getCurrentEntry()['name'])
print(4,m.getCurrentMenuSize())


print('')
print(m.getCurrentEntry()['name'])
print('')
print(m.getEntryForIndexCurrLevel(1)['name'])

m.nextEntry()
print(m.getCurrentEntry()['name'])
print(2,m.getCurrentMenuSize())
print('----')
m.enterMenu()
i = m.getCurrentEntry()
print(m.getCurrentEntry()['name'])
print(m.getEntryForIndexCurrLevel(1)['name'])
print(m.getCurrentEntry()['name'])
print('----')
print('----')
print('----')

print(4,m.getCurrentMenuSize())
'''

import sys, os, time, threading, curses
from pathlib import Path
from os.path import expanduser
from collections import OrderedDict
from dragonfilemanager.core import autoUpdateManager
from dragonfilemanager.core import favManager

class listManager():
    def __init__(self, id, dragonfmManager, pwd= ''):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.height = self.dragonfmManager.getScreenHeight()
        self.width = self.dragonfmManager.getScreenWidth()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.commandManager = self.dragonfmManager.getCommandManager()
        self.clipboardManager = self.dragonfmManager.getClipboardManager()
        self.autoUpdateManager = autoUpdateManager.autoUpdateManager(self.dragonfmManager)
        self.favManager = favManager.favManager(self.dragonfmManager)
        self.id = id
        self.location = ''
        self.collectorLocation = ''
        self.collectorIdentity = ''
        self.Path = None
        self.collector = None
        self.collectorParam = {}
        self.index = 0
        self.entries = OrderedDict()
        self.keys = None
        self.selection = []
        self.typeAheadSearch = ''
        self.lastTypeAheadTime = time.time()
        self.history = []
        self.historyIndex = -1
        self.isHistoryTracking = True
        self.requestReload = False
        self.requestReloadLock = threading.RLock()
        self.selectionMode = 0 # 0 = unselect on navigation, 1 = select on navigation, 2 = ignore
        self.page = 0
        self.columns = []
        self.setColumns(self.settingsManager.get('folder', 'columns'))
        self.sorting = []
        self.reverseSorting = False
        self.caseSensitiveSorting = False
        self.setSorting(self.settingsManager.get('folder', 'sorting'))
        self.setReverseSorting(self.settingsManager.getBool('folder', 'reverse'))
        self.setCaseSensitiveSorting(self.settingsManager.getBool('folder', 'casesensitive'))
        self.setCollector()
        self.initLocation(pwd)
    def shutdown(self):
        # stop watchdog
        try:
            self.autoUpdateManager.requestStop()
        except:
            pass
    def doTypeAheadSearch(self, key):
        # useful for type ahead search?
        if key == None:
            return False
        if not isinstance(key, str):
            return False
        if len(key) != 1:
            return False
        key = key.lower()
        if not key in '.-_0123456789abcdefghijklmnopqrstuvwxyz':
            return False
        if self.keys == None:
            return False
        if len(self.keys) < 2:
            return False
        # then search
        if self.typeAheadSearch != key:
            self.typeAheadSearch += key

        startIndex = self.getIndex()
        searchIndex = startIndex

        searchString = '{0}'.format(self.typeAheadSearch)

        while True:
            if len(self.typeAheadSearch) == 1:
                # jump always to next match if only one first letter nav (==1)
                searchIndex += 1
                if searchIndex >= len(self.keys):
                    searchIndex = 0
                if searchIndex == startIndex:
                    return False
            # search by name column
            entry = self.entries[self.keys[searchIndex]]
            if entry['name'].lower().startswith(searchString):
                self.setIndex(searchIndex)
                self.lastTypeAheadTime = time.time()
                return True
            elif len(self.typeAheadSearch) > 1:
                # keep current match until its not matching 
                # anymore for type ahead search (> 1)
                searchIndex += 1
                if searchIndex >= len(self.keys):
                    searchIndex = 0
                if searchIndex == startIndex:
                    return False
    def resetTypeAheadSearch(self, force = False):
        if (time.time() - self.lastTypeAheadTime > 1.5) or force:
            self.typeAheadSearch = ''
    def setColumns(self, colums):
        if isinstance(colums, str):
            colums = colums.lower().split(',')
        self.columns = colums
        if self.columns == []:
            self.columns = ['name','selected', 'clipboard']
    def getColumns(self):
        return self.columns
    def setSorting(self, sorting):
        if isinstance(sorting, str):
            self.sorting = sorting.split(',')
        self.sorting = sorting
        if self.sorting == []:
            self.sorting = ['name']

    def setSelectionMode(self, mode):
        self.selectionMode = mode
    def getSelectionMode(self):
        return self.selectionMode
    def nextSelectionMode(self):
        mode = self.getSelectionMode()
        mode += 1
        if mode > 2:
            mode = 0
        self.setSelectionMode(mode)
    def setReverseSorting(self, reverseSorting):
        try:
            self.reverseSorting = reverseSorting
        except:
            pass
    def setCaseSensitiveSorting(self, caseSensitiveSorting):
        try:
            self.caseSensitiveSorting = caseSensitiveSorting
        except:
            pass
    def initLocation(self, pwd):
        currFolder = expanduser(pwd)
        if (currFolder == '') or not os.access(currFolder, os.R_OK):
            currFolder = os.getcwd()
            if (currFolder == '') or not os.access(currFolder, os.R_OK):
                currFolder = expanduser(self.settingsManager.get('folder', 'pwd'))
                if (currFolder == '') or not os.access(currFolder, os.R_OK):
                    currFolder = expanduser("~")
                    if (currFolder == '') or not os.access(currFolder, os.R_OK):
                        currFolder = '/'
        self.gotoFolder(currFolder)
    def enter(self):
        self.dragonfmManager.update()
    def leave(self):
        pass
    def isRequestReload(self):
        self.requestReloadLock.acquire(True)
        requestReload = self.requestReload
        self.requestReloadLock.release()
        return requestReload
    def setRequestReload(self):
        self.requestReloadLock.acquire(True)
        self.requestReload = True
        self.requestReloadLock.release()
    def resetRequestReload(self):
        self.requestReloadLock.acquire(True)
        self.requestReload = False
        self.requestReloadLock.release()
    def setCurrentCursor(self, index, entryName = None):
        NoOfEntries = len(self.keys)
        # dont overrunt
        if index >= NoOfEntries:
            # dont underrun
            if NoOfEntries > 0:
                index = len(self.keys) - 1
            else:
                index = 0
        self.setIndex(index)

        # try to get current element 
        if entryName != None:
            try:
                self.setIndex( self.keys.index(entryName))
            except:
                pass
    def setLocation(self, location):
        self.Path = Path(location)
        self.location = location
        self.setIndex(0)
        return True
    def getKeyByIndex(self, index):
        try:
            return self.keys[index]
        except Exception as e:
            pass
        return None

    def updatePage(self):
        index = self.getIndex()
        size = self.getEntryAreaSize()
        page = int(index / size)
        if page != self.page:
            self.page = page

    def getIndex(self):
        return self.index
    def setIndex(self, index):
        self.index = index
    def firstEntry(self):
        self.setIndex(0)
    def lastEntry(self):
        if len(self.entries) - 1 >= 0:
            self.setIndex(len(self.entries) - 1)
        else:
            self.setIndex(0)
    def prevEntry(self):
        if self.getIndex() > 0:
            self.setIndex( self.getIndex() -1)
        else:
            self.firstEntry()
    def nextEntry(self):
        if self.index < len(self.entries) - 1:
            self.setIndex( self.getIndex() +1)
        else:
            self.lastEntry()
    def getEntryAreaSize(self):
        return self.height - self.dragonfmManager.getHeaderOffset()
    def parentEntry(self):
        location = self.getLocation()
        if location.endswith('/'):
            location = location[:-1]
        if self.favManager.isFavoritFolder(location):
            return False
        if location == '':
            return False
        path = os.path.dirname(location)
        if path == '':
            return False
        self.openEntry(path, location)
        return True
    def openEntry(self, path, entryName=None, entry = None):
        if not path:
            return
        if path == '':
            return
        if os.path.isdir(path):
            if self.favManager.isFavoritFolder(self.getLocation()):
                if os.path.islink(path):
                    path = os.path.realpath(path)
            self.setCollector()
            self.gotoFolder(path, entryName)
        else:
            self.fileManager.openFile(entry, self.getLocation())
    
    def getCurrentEntry(self):
        try:
            return self.entries[self.getCurrentKey()]
        except:
            return None
    def getCurrentKey(self):
        try:
            return self.getKeyByIndex(self.getIndex())
        except:
            return None

    def getPositionForIndex(self):
        index = self.getIndex()
        size = self.getEntryAreaSize()
        page = self.getPage()
        # page to index
        screenIndex = index - page * size
        # header bar
        screenIndex += self.dragonfmManager.getHeaderOffset()
        return screenIndex
    def update(self):
        if self.isRequestReload():
            self.reloadFolder()
        self.drawHeader()
        self.updatePage()
        self.drawEntryList()
        screenIndex = self.getPositionForIndex()
        self.dragonfmManager.setCursor(screenIndex, 0)
        self.dragonfmManager.refresh()
    def getID(self):
        return self.id
    def getPage(self):
        return self.page
    def gotoFolder(self, path, entryName = None):
        if self.loadEntriesFromFolder(path, entryName):
            return True
        return False
    def reloadFolder(self):
        entryName = self.getCurrentKey()
        self.gotoFolder(self.getLocation(), entryName)
    def defaultCollector(self, param):
        path = param['path']
        elements = os.listdir(path)
        showHidden = self.settingsManager.getBool('folder', 'showHidden')
        entries = {}
        for e in elements:
            if not showHidden:
                if e.startswith('.'):
                    continue
            fullPath = path
            if not fullPath.endswith('/'):
                fullPath += '/'
            fullPath += e
            entry = self.fileManager.getInfo(fullPath)
            if entry != None:
                entries[fullPath] = entry
        return entries, param['path']

    def getCollectorLocation(self):
        return self.collectorLocation

    def setCollectorLocation(self, collectorLocation):
        if self.getCollectorLocation() == '':
            self.collectorLocation = collectorLocation

    def resetCollectorLocation(self):
        self.CollectorLocation = ''
    def getCollectorIdentity(self):
        return self.collectorIdentity
    def setCollector(self, collector=None, collectorParam = {}, collectorIdentity = 'folderList'):
        if collector == None:
            collector = self.defaultCollector
            self.setColumns(self.settingsManager.get('folder', 'columns'))
            self.resetCollectorLocation()
        else:
            self.setCollectorLocation(self.getLocation())
        self.collector = collector
        self.collectorParam = collectorParam
        self.collectorIdentity = collectorIdentity
    def getCollector(self):
        return self.collector
    def getCollectorParam(self):
        return self.collectorParam
    def loadEntriesFromFolder(self, path, entryName = None):
        self.resetRequestReload()
        if path == '':
            return False
        if not self.getCollector():
            return False     
        path = expanduser(path)
        if path.endswith('/') and path != '/':
            path = path[:-1]
        locationChanged = path != self.getLocation()
        if not os.access(path, os.R_OK):
            if not locationChanged:
                self.unselectAllEntries()
                entries = {}
            return False
        if not os.path.isdir(path):
            if not locationChanged:
                self.unselectAllEntries()
                entries = {}
            return False

        # stop watchdog
        try:
            self.autoUpdateManager.requestStop()
        except:
            pass
        # unselect on new location and track history
        if locationChanged:
            self.trackHistory()
            self.unselectAllEntries()
        # collect data
        collectorParam = self.getCollectorParam()
        collectorParam['path'] = path
        collectorParam['folderManager'] = self
        entries, newPath = self.getCollector()(collectorParam)

        locationChanged = newPath != self.getLocation()
        # set new location
        if locationChanged:
            self.setLocation(newPath)
        # do sorting and place cursor
        self.createdSortedEntries(entries)
        self.setCurrentCursor(self.getIndex(), entryName)
        # wait and [re]start watchdog
        try:
            self.autoUpdateManager.waitForStopWatch()
        except:
            pass
        try:
            self.autoUpdateManager.startWatch(newPath, self.setRequestReload)
        except:
            pass
        return True
    def createdSortedEntries(self, entries):
        self.entries = OrderedDict(sorted(entries.items(), reverse=self.reverseSorting, key=self.getSortingKey))
        self.keys = tuple(self.entries.keys())
    def getSortingKey(self, element):
        #self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, str(element))
        sortingKey = []
        try:
            for column in self.sorting:
                if isinstance(element[1][column], str):
                    if self.caseSensitiveSorting:
                        sortingKey.append(element[1][column])
                    else:
                        sortingKey.append(element[1][column].lower())
                else:
                    sortingKey.append(element[1][column])
        except:
            return element[0]
        return sortingKey
    def handleFolderInput(self, shortcut):
        command = self.settingsManager.getShortcut(self.getCollectorIdentity()+'-keyboard', shortcut)
        debug = self.settingsManager.getBool('debug', 'input')
        self.resetTypeAheadSearch(command != '')
        if command == '':
            if debug:
                self.dragonfmManager.setMessage('debug Sequence: {0}'.format(shortcut))
            if self.doTypeAheadSearch(shortcut):
                return True
            return False
        try:
            if not self.commandManager.isCommandActive(self.getCollectorIdentity(), command):
                return False
            result = self.commandManager.runCommand(self.getCollectorIdentity(), command)
            if debug:
                self.dragonfmManager.setMessage('debug Sequence: {0} Command: {1} Command Success: {2}'.format(shortcut, command, result))
            return result
        except Exception as e:
            if debug:
                self.dragonfmManager.setMessage('debug Sequence: {0} Command: {1} Error: {2}'.format(shortcut, command, e))
    def handleInput(self, shortcut):
        return self.handleFolderInput(shortcut)
    def getLocation(self):
        return self.location

    def drawHeader(self):
        # paint header
        self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, _('Tab: {0} List').format(self.getID()))
        self.dragonfmManager.incHeaderOffset()
        location = self.getLocation()
        if not self.favManager.isFavoritFolder(location):
            self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, _('Location: {0}').format(location))
        else:
            self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, _('Location: {0}'.format(_('Favorits'))))

        self.dragonfmManager.incHeaderOffset()
        self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset(), 0, _('Page: {0}').format(self.getPage() + 1))
        self.dragonfmManager.incHeaderOffset()
    def selectEntry(self, key):
        if not key:
            return False
        if key == '':
            return False
        if not key in self.keys:
            return False
        if not self.isSelected(key):
            try:
                self.selection.append(key)
                return True
            except:
                pass
        return False
    def unselectEntry(self, key):
        if self.isSelected(key):
            try:
                self.selection.remove(key)
                return True
            except:
                pass
        return False
    def selectCurrentEntry(self):
        key = self.getCurrentKey()
        return self.selectEntry(key)
    def uncselectCurrentEntry(self):
        key = self.getCurrentKey()
        return self.unselectEntry(key)
    def isCurrentEntrySelected(self):
        key = self.getCurrentKey()
        return self.isSelected(key)
    def selectAllEntries(self):
        self.unselectAllEntries()
        self.selection = list(self.keys)
        return self.selection != []
    def unselectAllEntries(self):
        if self.selection != []:
            self.selection = []
            return True
        return False
    def isSelected(self, key):
        return key in self.selection
    def getSelection(self):
        return self.selection.copy()
    def drawEntryList(self):
        startingIndex = self.getPage() * self.getEntryAreaSize()
        pos = 0
        for c in self.getColumns():
            columnLen = len(c) + 2
            for i in range(self.getEntryAreaSize()):
                if i == self.height:
                    break
                if startingIndex + i >= len(self.entries):
                    break
                key = self.getKeyByIndex(startingIndex + i)
                formattedValue = ''
                if c == 'selected':
                    formattedValue = self.calcSelectionColumn(key)
                elif c == 'clipboard':
                    formattedValue = self.calcClipboardColumn(key)
                else:
                    e = self.entries[key]
                    formattedValue = self.fileManager.formatColumn(c, e[c])
                if columnLen < len(formattedValue) + 2:
                    columnLen = len(formattedValue) + 2
                self.dragonfmManager.addText(i + self.dragonfmManager.getHeaderOffset(), pos, formattedValue )
                i += 1
            self.dragonfmManager.addText(self.dragonfmManager.getHeaderOffset() - 1, pos, c )
            pos += columnLen

    def calcClipboardColumn(self, entry = ''):
        if entry == '':
            return ''
        clipboard = self.clipboardManager.getClipboard()
        if entry in clipboard:
            return self.clipboardManager.getOperation()
        return ''
    def calcSelectionColumn(self, entry):
        if entry == '':
            return ''
        if self.isSelected(entry):
            return 'selected'
        return ''
    # History Tracking
    def getIsHistoryTracking(self):
        return self.isHistoryTracking
    def setIsHistoryTracking(self, isTracking):
        self.isHistoryTracking = isTracking
    def trackHistory(self):
        if not self.getIsHistoryTracking():
            return
        self.history = self.getHistory()[:self.getHistoryIndex() + 1]
        location = self.getLocation()
        entryName = self.getCurrentKey()
        self.history.append([location, entryName])
        self.setHistoryIndex(len(self.getHistory()) - 1)
    def getHistory(self):
        return self.history
    def isHistoryEmpty(self):
        return len(self.getHistory()) == 0
    def firstHistory(self):
        if self.isHistoryEmpty():
            return
        self.setIsHistoryTracking(False)
        self.setHistoryIndex(0)
        historyEntry = self.getCurrHistoryEntry()
        location = historyEntry[0]
        entryName = historyEntry[1]
        self.gotoFolder(location, entryName)
        self.setIsHistoryTracking(True)
    def lastHistory(self):
        if self.isHistoryEmpty():
            return
        self.setIsHistoryTracking(False)
        self.setHistoryIndex( len(self.getHistory()) - 1)
        historyEntry = self.getCurrHistoryEntry()
        location = historyEntry[0]
        entryName = historyEntry[1]
        self.gotoFolder(location, entryName)
        self.setIsHistoryTracking(True)
    def prevHistory(self):
        if self.isHistoryEmpty():
            return
        self.setIsHistoryTracking(False)
        if self.getHistoryIndex() - 1 < 0:
            self.firstHistory()
        else:
            self.setHistoryIndex(self.historyIndex - 1)
            historyEntry = self.getCurrHistoryEntry()
            location = historyEntry[0]
            entryName = historyEntry[1]
            self.gotoFolder(location, entryName)
        self.setIsHistoryTracking(True)
    def nextHistory(self):
        if self.isHistoryEmpty():
            return
        self.setIsHistoryTracking(False)
        if self.getHistoryIndex() + 1 >= len(self.getHistory()) -1:
            self.lastHistory()
        else:
            self.setHistoryIndex(self.historyIndex + 1)
            historyEntry = self.getCurrHistoryEntry()
            location = historyEntry[0]
            entryName = historyEntry[1]
            self.gotoFolder(location, entryName)
        self.setIsHistoryTracking(True)

    def getCurrHistoryEntry(self):
        return self.getHistory()[self.getHistoryIndex()]
    def setHistoryIndex(self, index):
        self.historyIndex = index
    def getHistoryIndex(self):
        return self.historyIndex

import sys, os, time, threading, curses
from pathlib import Path
from os.path import expanduser
from collections import OrderedDict
from dragonfilemanager.core import autoUpdateManager

class folderManager():
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
        self.id = id
        self.message = ''
        self.location = ''
        self.Path = None
        self.keyDebugging = False
        self.collector = None
        self.collectorParam = {}
        self.index = 0
        self.entries = OrderedDict()
        self.keys = None
        self.selection = []
        self.typeAheadSearch = ''
        self.lastTypeAheadTime = time.time()
        self.headerOffset = 0
        self.footerOffset = 0
        self.messageTimer = None
        self.requestReload = False
        self.requestReloadLock = threading.RLock()
        self.selectionMode = 0 # 0 = unselect on navigation, 1 = select on navigation, 2 = ignore
        self.page = 0
        self.columns = ['name','selected', 'clipboard']
        self.setColumns(self.settingsManager.get('folder', 'columns'))
        self.sorting = ['name']
        self.reverseSorting = False
        self.caseSensitiveSorting = False
        self.setSorting(self.settingsManager.get('folder', 'sorting'))
        self.setReverseSorting(self.settingsManager.getBool('folder', 'reverse'))
        self.setCaseSensitiveSorting(self.settingsManager.getBool('folder', 'casesensitive'))
        self.setCollector()
        self.initLocation(pwd)
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
    def setColumns(self, columsString):
        self.columns = columsString.split(',')
        if self.columns == '':
            self.columns = ['name','selected']
    def setSorting(self, sortingString):
        try:
            self.sorting = sortingString.split(',')
            if self.sorting == '':
                self.sorting = ['name']
        except:
            pass
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
        return self.height - self.headerOffset- self.footerOffset
    def parentEntry(self):
        location = self.getLocation()
        if location.endswith('/'):
            location = location[:-1]
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
        screenIndex += self.headerOffset
        return screenIndex
    def update(self):
        if self.isRequestReload():
            self.reloadFolder()
        self.dragonfmManager.erase()
        self.drawHeader()
        self.drawFooter()
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
    def currFolderCollector(self, param):
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
        return entries
    def setCollector(self, collector=None, collectorParam = {}):
        if collector == None:
            collector = self.currFolderCollector
        self.collector = collector
        self.collectorParam = collectorParam
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
        # unselect on new location
        if locationChanged:
            self.unselectAllEntries()
        # collect data
        collectorParam = self.getCollectorParam()
        collectorParam['path'] = path
        entries = self.getCollector()(collectorParam)
        # set new location
        if locationChanged:
            self.setLocation(path)
        # do sorting and place cursor
        self.createdSortedEntries(entries)
        self.setCurrentCursor(self.getIndex(), entryName)
        # wait and [re]start watchdog
        try:
            self.autoUpdateManager.waitForStopWatch()
        except:
            pass
        try:
            self.autoUpdateManager.startWatch(path, self.setRequestReload)
        except:
            pass
        return True
    def createdSortedEntries(self, entries):
        self.entries = OrderedDict(sorted(entries.items(), reverse=self.reverseSorting, key=self.getSortingKey))
        self.keys = tuple(self.entries.keys())
    def getSortingKey(self, element):
        #self.screen.addstr(self.headerOffset, 0, str(element))
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
        command = self.settingsManager.getShortcut('folder-keyboard', shortcut)
        debug = self.settingsManager.getBool('debug', 'input')
        self.resetTypeAheadSearch(command != '')
        if command == '':
            if debug:
                self.setMessage('debug Sequence: {0}'.format(shortcut))
            if self.doTypeAheadSearch(shortcut):
                return True
            return False
        try:
            result = self.commandManager.runCommand('folder', command)
            if debug:
                self.setMessage('debug Sequence: {0} Command: {1} Command Success: {2}'.format(shortcut, command, result))
            return result
        except Exception as e:
            if debug:
                self.setMessage('debug Sequence: {0} Command: {1} Error: {2}'.format(shortcut, command, e))
    def handleInput(self, shortcut):
        return self.handleFolderInput(shortcut)
    def getLocation(self):
        return self.location
    def showMessage(self):
        if self.isMessage():
            self.screen.addstr(self.height - self.footerOffset, 0, self.message)
    def isMessage(self):
        return self.message != ''
    def resetMessage(self):
        self.message = ''
    def setMessage(self, message):
        if self.messageTimer:
            if self.messageTimer.is_alive():
                self.messageTimer.cancel()
        self.messageTimer = threading.Timer(0.5, self.resetMessage)
        self.message = message
        self.messageTimer.start()
    def drawHeader(self):
        self.headerOffset = 0
        # paint header
        self.screen.addstr(self.headerOffset, 0, _('Tab: {0}').format(self.getID()))
        self.headerOffset += 1
        self.screen.addstr(self.headerOffset, 0, _('Location: {0}').format(self.getLocation()))
        self.headerOffset += 1
        self.screen.addstr(self.headerOffset, 0, _('Page: {0}').format(self.getPage() + 1))
        self.headerOffset += 1
        pos = 0
        for c in self.columns:
            self.screen.addstr(self.headerOffset, pos, c )
            pos += len(c) + 3
        self.headerOffset += 1
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
        for i in range(self.getEntryAreaSize()):
            if i == self.height - self.footerOffset:
                break
            if startingIndex + i >= len(self.entries):
                break
            key = self.getKeyByIndex(startingIndex + i)
            e = self.entries[key]
            pos = 0
            #debug
            #self.screen.addstr(i + self.headerOffset, pos, key)
            #continue
            for c in self.columns:
                lowerColumn = c.lower()
                if lowerColumn == 'selected':
                    value = self.calcSelectionColumn(key)
                    self.screen.addstr(i + self.headerOffset, pos, value)
                    pos += len(value) + 2
                elif lowerColumn == 'clipboard':
                    #continue
                    value = self.calcClipboardColumn(key)
                    self.screen.addstr(i + self.headerOffset, pos, value)
                    pos += len(value) + 2
                else:
                    formattedValue = self.fileManager.formatColumn(lowerColumn, e[lowerColumn])
                    if i + len(formattedValue) < self.width:
                        self.screen.addstr(i + self.headerOffset, pos, formattedValue )
                        pos += len(formattedValue) + 2
            i += 1
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
    def drawFooter(self):
        self.footerOffset = 0
        self.footerOffset += 1
        self.showMessage()

import sys, os, time, threading, curses, math
from pathlib import Path
from os.path import expanduser
from collections import OrderedDict

class folderManager():
    def __init__(self, id, dragonfmManager, pwd= ''):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.height = self.dragonfmManager.getScreenHeight()        
        self.width = self.dragonfmManager.getScreenWidth()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.commandManager = self.dragonfmManager.getCommandManager()
        self.id = id
        self.message = ''
        self.location = ''
        self.Path = None
        self.keyDebugging = False
        self.index = 0
        self.entries = OrderedDict()
        self.keys = []
        self.selection = []
        self.typeAheadSearch = ''
        self.lastTypeAheadTime = time.time()
        self.headerOffset = 0
        self.footerOffset = 0
        self.messageTimer = None
        self.needRefresh = False
        self.selectionMode = 0 # 0 = unselect on navigation, 1 = select on navigation, 2 = ignore
        self.page = 0
        self.columns = ['name','selected']
        self.setColumns(self.settingsManager.get('folder', 'columns'))
        self.sorting = ['name']
        self.reverseSorting = False
        self.caseSensitiveSorting = False
        self.setSorting(self.settingsManager.get('folder', 'sorting'))
        self.setReverseSorting(self.settingsManager.getBool('folder', 'reverse'))
        self.setCaseSensitiveSorting(self.settingsManager.getBool('folder', 'casesensitive'))
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
        location = self.getLocation()
        if not location.endswith('/'):
            location += '/'
        searchString = '{0}{1}'.format(location, self.typeAheadSearch)
        
        while True:
            if len(self.typeAheadSearch) == 1:
                # jump always to next match if only one first letter nav (==1)
                searchIndex += 1
                if searchIndex >= len(self.keys):
                    searchIndex = 0
                if searchIndex == startIndex:
                    return False
            if self.keys[searchIndex].lower().startswith(searchString):
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

    def removeEntry(self, path):
        try:
            self.selection.remove(path)
        except:
            pass        
        try:
            self.keys.remove(path)
        except:
            pass
        try:
            del(self.entries[path])
        except:
            pass
        entry = self.getCurrentEntry(self)
        if entry == None:
            self.lastEntry()
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
        self.setNeedRefresh()
        self.dragonfmManager.update()
    def leave(self):
        pass
    def setNeedRefresh(self):
        self.needRefresh = True
    def setLocation(self, location, entryName = None):
        if location == '':
            return False
        if not os.path.exists(location):
            return False
        self.Path = Path(location)
        self.location = location
        self.setIndex(0)
        if entryName != None:
            try:
                self.setIndex( self.keys.index(entryName))
            except:
                pass
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
            self.setNeedRefresh()
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
        self.setNeedRefresh()
        return True
    def openEntry(self, path, entryName=None, entry = None):
        if not path:
            return
        if path == '':
            return
        if os.path.isdir(path):
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
        if self.needRefresh:
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
        if self.loadEntriesFromFolder(path):
            self.setLocation(path, entryName)
            self.setNeedRefresh()
            return True
        return False
    def reloadFolder(self):
        entryName = self.getCurrentKey()
        self.gotoFolder(self.getLocation(), entryName)
    def loadEntriesFromFolder(self, path):
        if path != self.getLocation():
            self.unselectAllEntries()
        if not os.access(path, os.R_OK):
            return False
        if not path.endswith('/'):
            path += '/'
        elements = os.listdir(path)
        entries = {}
        for e in elements:
            if e.startswith('.'):
                if not self.settingsManager.getBool('folder', 'showHidden'):
                    continue
            fullPath = path + e
            entry = self.fileManager.getInfo(fullPath)
            if entry != None:
                entries[fullPath] = entry
        # sort entries here
        self.createdSortedEntries(entries)
        return True
    def createdSortedEntries(self, entries):
        self.entries = OrderedDict(sorted(entries.items(), reverse=self.reverseSorting, key=self.getSortingKey))
        self.keys = list(self.entries.keys())
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
        self.setNeedRefresh()
        self.dragonfmManager.update()
    def setMessage(self, message):
        if self.messageTimer:
            if self.messageTimer.is_alive():
                self.messageTimer.cancel()
        self.messageTimer = threading.Timer(0.5, self.resetMessage)

        self.message = message
        self.setNeedRefresh()
        self.dragonfmManager.update()
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
        selected = False
        for key in self.keys:
            if self.selectEntry(key):
                selected = True
        return selected
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
        for i in range(self.getEntryAreaSize()):
            if i == self.height - self.footerOffset:
                break
            if self.getPage() * self.getEntryAreaSize() + i >= len(self.entries):
                break
            key = self.getKeyByIndex(self.getPage() * self.getEntryAreaSize() + i)
            e = self.entries[key]
            pos = 0
            #debug
            #self.screen.addstr(i + self.headerOffset, pos, key)
            #continue
            for c in self.columns:
                lowerColumn = c.lower()
                if lowerColumn == 'selected':
                    if self.isSelected(key):
                        self.screen.addstr(i + self.headerOffset, pos, 'selected')
                        pos += len('selected') + 2
                else:
                    formattedValue = self.fileManager.formatColumn(lowerColumn, e[lowerColumn])
                    if i + len(formattedValue) < self.width:
                        self.screen.addstr(i + self.headerOffset, pos, formattedValue )
                        pos += len(formattedValue) + 2
            i += 1

    def drawFooter(self):
        self.footerOffset = 0
        self.footerOffset += 1
        self.showMessage()

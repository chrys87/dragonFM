import sys, os, time, threading, curses, math
from pathlib import Path
from os.path import expanduser
from operator import itemgetter 
from collections import OrderedDict

class folderManager():
    def __init__(self, id, dragonfmManager, pwd= ''):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.commandManager = self.dragonfmManager.getCommandManager()
        self.id = id
        self.message = ''
        self.location = ''
        self.Path = None
        self.index = 0
        self.entries = OrderedDict()
        self.keys = []
        self.selection = []
        self.headerOffset = 0
        self.footerOffset = 0
        self.messageTimer = None
        self.needRefresh = False
        self.height = self.dragonfmManager.getScreenHeight()
        self.page = 0
        self.columns = ['name','selected']
        self.setColumns(self.settingsManager.get('folder', 'columns'))
        self.sorting = ['name']
        self.reverseSorting = False
        self.setSorting(self.settingsManager.get('folder', 'sorting'))
        self.setReverse(self.settingsManager.getBool('folder', 'reverse'))
        self.initLocation(pwd)
    def setColumns(self, columsString):
        self.columns = self.settingsManager.get('folder', 'columns')
        if self.columns == '':
            self.columns = 'name,selected'        
    def setSorting(self, sortingString):
        try:
            self.sorting = sortingString
            if self.sorting == '':
                self.sorting = 'name'
            self.sorting = self.sorting.split(',')
        except:
            pass     
    def setReverse(self, reverseSorting):
        try:
            self.reverseSorting = reverseSorting        
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
        self.update()
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
        self.index = 0
        if entryName != None:
            try:
                self.index = self.keys.index(entryName)
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
    def firstEntry(self):
        self.index = 0
    def lastEntry(self):
        if len(self.entries) - 1 >= 0:
            self.index = len(self.entries) - 1
        else:
            self.index = 0
    def prevEntry(self):
        if self.index > 0:
            self.index -= 1
        else:
            self.firstEntry()
    def nextEntry(self):
        if self.index < len(self.entries) - 1:
            self.index += 1
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
        entryName = os.path.basename(location)
        self.openEntry(path, entryName)
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
        return self.getKeyByIndex(self.getIndex())    

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
            self.dragonfmManager.clear()
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
        self.gotoFolder(self.getLocation())
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
        self.createdSortedEntries()
        return True
    def createdSortedEntries(self, entries, key=None, reverse=None):    
        if key == None:
            key = self.sorting
        if reverse == None:
            reverse = self.reverse
        self.entries = OrderedDict(sorted(e.items(), reverse=reverse, key=lambda t: t[0]))
        self.keys = list(entries.keys())
    def handleFolderInput(self, shortcut):
        command = self.settingsManager.getShortcut('folder-keyboard', shortcut)
        if command == '':
            #self.setMessage(shortcut)
            return False
        return self.commandManager.runCommand('folder', command)

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
        self.update()
    def setMessage(self, message):
        if self.messageTimer:
            if self.messageTimer.is_alive():
                self.messageTimer.cancel()
        self.messageTimer = threading.Timer(0.5, self.resetMessage)

        self.message = message
        self.setNeedRefresh()
        self.update()
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
            return
        if key == '':
            return
        if not key in self.keys:
            return
        if not self.isSelected(key):
            try:
                self.selection.append(key)
            except:
                pass
    def unselectEntry(self, key):
        if self.isSelected(key):
            try:
                self.selection.remove(key)
            except:
                pass
    def selectCurrentEntry(self):
        key = self.getCurrentKey()
        self.selectEntry(key)
    def selectAllEntries(self):
        for key in self.keys:
            self.selectEntry(key)            
    def unselectAllEntries(self):
        self.selection = []
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
                if c.lower() == 'selected':
                    if self.isSelected(key):
                        self.screen.addstr(i + self.headerOffset, pos, 'selected')
                        pos += len('selected') + 3
                else:
                    self.screen.addstr(i + self.headerOffset, pos, e[c] )
                    pos += len(e[c]) + 3
            i += 1

    def drawFooter(self):
        self.footerOffset = 0
        self.footerOffset += 1
        self.showMessage()

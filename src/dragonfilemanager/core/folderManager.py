import sys, os, time, threading, curses, math
from pathlib import Path
from os.path import expanduser

class folderManager():
    def __init__(self, id, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.startUpManager = self.dragonfmManager.getStartUpManager()
        self.id = id
        self.message = ''
        self.location = ''
        self.Path = None
        self.setLocation(expanduser("~"))
        self.selection = []
        self.index = 0
        self.entries = {}
        self.keys = []
        self.loadentriesFromFolder(self.getLocation())
        self.headerOffset = 0
        self.footerOffset = 0
        self.messageTimer = None
        self.needRefresh = True
        self.height = self.dragonfmManager.getScreenHeight()
        self.page = 0
        self.columns = self.settingsManager.getShortcut('folder', 'columns')
        if self.columns == '':
            self.columns = name
        self.columns = self.columns.split(',')
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
            return str(e)
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
    def prevEntry(self):
        if self.index > 0:
            self.index -= 1
    def nextEntry(self):
        if self.index < len(self.entries) - 1:
            self.index += 1
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
    def openEntry(self, path, entryName=None, force = False):
        if os.path.isdir(path) or force:
            if self.loadentriesFromFolder(path):
                self.setLocation(path, entryName)
                self.setNeedRefresh()
        else:
            self.fileManager.openFile(path)
    def getCurrentEntry(self):
        try:
            return self.entries[self.getKeyByIndex(self.getIndex())]
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
    def reloadFolder(self):
        self.loadentriesFromFolder(self.getLocation())
    def loadentriesFromFolder(self, path):
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
                entries[e] = entry
        # sort entries here
        self.entries = entries
        self.keys = list(entries.keys())
        self.setLocation(path)
        return True

    def handleFolderInput(self, shortcut):
        command = self.settingsManager.getShortcut('folder-keyboard', shortcut)
        #if command == '':
        #    return False
        #return self.commandManager.runCommand('folder', command)

        #self.setMessage(key)
        if shortcut == 'KEY_UP':
            self.prevEntry()
            return True
        elif shortcut == 'KEY_DOWN':
            self.nextEntry()
            return True
        elif shortcut == 'KEY_RIGHT':
            self.openEntry(self.getCurrentEntry()['full'])
            return True
        elif shortcut == 'KEY_LEFT':
            self.parentEntry()
            return True
        return False
    def handleInput(self, shortcut):
        return self.handleFolderInput(shortcut)
    def getSelection(self):
        if self.selection == []:
            return [self.getEntry()]
        return self.selection
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

    def drawEntryList(self):

        for i in range(self.getEntryAreaSize()):
            if i == self.height - self.footerOffset:
                break
            if self.getPage() * self.getEntryAreaSize() + i >= len(self.entries):
                break
            e = self.entries[self.getKeyByIndex(self.getPage() * self.getEntryAreaSize() + i)]
            pos = 0
            for c in self.columns:
                self.screen.addstr(i + self.headerOffset, pos, e[c] )
                pos += len(e[c]) + 3
            i += 1

    def drawFooter(self):
        self.footerOffset = 0
        self.footerOffset += 1
        self.showMessage()

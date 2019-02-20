import sys, os, time, threading, curses, math
from os.path import expanduser

class folderManager():
    def __init__(self, id, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.id = id
        self.message = ''
        self.location = expanduser("~")
        self.selection = []
        self.index = [0]
        self.folderList = []
        self.loadFolder(self.getLocation())
        self.headerOffset = 0
        self.footerOffset = 0
        self.messageTimer = None
        self.needRefresh = True
        self.height = self.dragonfmManager.getScreenHeight()
        self.page = 0
    def enter(self):
        self.setNeedRefresh()
        self.draw()
    def leave(self):
        pass
    def setNeedRefresh(self):
        self.needRefresh = True
    def updatePage(self):
        index = self.getCurrentIndex()
        size = self.getFolderAreaSize()
        page = int(index / size)
        if page != self.page:
            self.setNeedRefresh()
            self.page = page
    def getCurrentLevel(self):
        return len(self.index) - 1
    def getCurrentIndex(self):
        return self.index[len(self.index) - 1]
    def prevElement(self):
        if self.index[self.getCurrentLevel()] > 0:
            self.index[self.getCurrentLevel()] -= 1
    def nextElement(self):
        if self.index[self.getCurrentLevel()] < len(self.folderList) - 1:
            self.index[self.getCurrentLevel()] += 1
    def getFolderAreaSize(self):
        return self.height - self.headerOffset- self.footerOffset
    def openElement(self, location):
        if not location.endswith('/'):
            location += '/'
        location += self.folderList[self.getCurrentIndex()]['name']
        if os.path.isdir(location):
            if self.loadFolder(location):
                self.index.append(0)
                self.setNeedRefresh()
        else:
            self.fileManager.openFile(location)
    def getPositionForIndex(self):
        index = self.getCurrentIndex()
        size = self.getFolderAreaSize()
        page = self.getPage()
        # page to index
        screenIndex = index - page * size
        # header bar
        screenIndex += self.headerOffset
        return screenIndex
    def draw(self):
        if self.needRefresh:
            self.dragonfmManager.clear()
            self.drawHeader()
            self.drawFooter()
            self.updatePage()
            self.drawFolderList()
        screenIndex = self.getPositionForIndex()
        self.dragonfmManager.move(screenIndex, 0)
        self.dragonfmManager.refresh()
    def getID(self):
        return self.id
    def getPage(self):
        return self.page
    def loadFolder(self, path):
        if not os.access(path, os.R_OK):
            return False
        folderList = []
        if not path.endswith('/'):
            path += '/'
        elements = os.listdir(path)
        for e in elements:
            fullPath = path + e
            entry = self.fileManager.getInfo(fullPath)
            if entry != None:
                folderList.append(entry)
        # sort folderList here
        self.folderList = folderList
        self.location = path
        return True

    def handleInput(self, key):
        #self.setMessage(key)
        if key == 'KEY_UP':
            self.prevElement()
            return True
        elif key == 'KEY_DOWN':
            self.nextElement()
            return True
        elif key == 'r':
            self.openElement(self.getLocation())
        return False
    def getEntry(self):
        return self.index[len(self.index) - 1]
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
        self.draw()
    def setMessage(self, message):
        if self.messageTimer:
            if self.messageTimer.is_alive():
                self.messageTimer.cancel()
        self.messageTimer = threading.Timer(0.5, self.resetMessage)

        self.message = message
        self.setNeedRefresh()
        self.draw()
        self.messageTimer.start()
    def drawHeader(self):
        self.headerOffset = 0
        # paint header
        self.screen.addstr(self.headerOffset, 0, _('Tab: {0}').format(self.getID()))
        self.headerOffset += 1
        self.screen.addstr(self.headerOffset, 0, _('Folder: {0}').format(self.getLocation()))
        self.headerOffset += 1
        self.screen.addstr(self.headerOffset, 0, _('Page: {0}').format(self.getPage() + 1))
        self.headerOffset += 1
    
    def drawFolderList(self):
        for i in range(self.getFolderAreaSize()):
            if i == self.height - self.footerOffset:
                break
            if self.getPage() * self.getFolderAreaSize() + i >= len(self.folderList):
                break
            e = self.folderList[self.getPage() * self.getFolderAreaSize() + i]
            self.screen.addstr(i + self.headerOffset, 0, e['name'] + ' ' + e['type'] )
            i += 1
        
    def drawFooter(self):
        self.footerOffset = 0
        self.footerOffset += 1
        self.showMessage()
        

import sys, os, time, threading, curses
from os.path import expanduser

class folderManager():
    def __init__(self, screen):
        self.screen = None
        self.height = 0
        self.width = 0
        self.message = ''
        self.setScreen(screen)
        self.location = expanduser("~")
        self.selection = []
        self.index = [0]
        self.folderList = []
        self.loadFolder(self.location)
        self.headerOffset = 1
        self.footerOffset = 1
        self.timer = threading.Timer(0.5, self.resetMessage)

    def enter(self):
        self.draw()
    def leave(self):
        pass
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
    def getFolderArea(self):
        return self.height - self.headerOffset- self.footerOffset
    def openElement(self):
        location = self.location
        if not location.endswith('/'):
            location += '/'
        location += self.folderList[self.getCurrentIndex()]['name']
        if os.path.isdir(location):
            if self.loadFolder(location):
                self.index.append(0)
        else:
            self.openFile(location)
    def openFile(self, path):
        pass
    def getPositionForIndex(self):
        return self.getCurrentIndex()
    def draw(self):
        #self.screen.scroll(self.getFolderArea())
        self.clear()
        self.screen.addstr(0, 0, 'Folder')
        self.showMessage()
        i = self.headerOffset
        for e in self.folderList:
            if i == self.height - self.footerOffset:
                break
            self.screen.addstr(i, 0, e['name'])
            i += 1
        self.screen.move(self.getPositionForIndex(), 0)
        self.refresh()


    def loadFolder(self, path):
        if not os.access(path, os.R_OK):
            return False
        folderList = []
        elements = os.listdir(path)
        for e in elements:
            entry = {'name': e}
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
            self.openElement()
        return False
    def refresh(self):
        self.screen.refresh()
    def clear(self):
        self.screen.clear()
    def setScreen(self, screen):
        if not screen:
            return
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()
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
        self.draw()
    def setMessage(self, message):
        #try:
        #    self.timer.cancel()
        #except:
        #    pass
        self.message = message
        self.timer.start()

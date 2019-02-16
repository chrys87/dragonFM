import sys, os, time, threading, curses
from os.path import expanduser

class folderManager():
    def __init__(self, id, screen, settingsManager):
        self.screen = None
        self.id = id
        self.settingsManager = settingsManager
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
        self.screen.addstr(0, 0, _('Tab: {0} Folder: {1}').format(self.id, self.location))
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
        if not path.endswith('/'):
            path += '/'
        elements = os.listdir(path)
        for e in elements:
            fullPath = path + e
            info = None
            try:
                info = os.stat(fullPath)
            except:
                pass
            entry = {'name': e,
             'full': fullPath,
             'path': path,
             'info': info
            }
            folderList.append(entry)
        # sort folderList here
        self.folderList = folderList
        self.location = path
        return True

    def handleInput(self, key):
        self.setMessage(key)
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
        if self.timer.is_alive():
            self.timer.cancel()
        self.timer = threading.Timer(0.5, self.resetMessage)

        self.message = message
        self.draw()
        if not self.timer.is_alive():
            self.timer.start()

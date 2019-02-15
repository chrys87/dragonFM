import sys, os, time
import curses
from os.path import expanduser

class folderManager():
    def __init__(self, screen):
        self.screen = None
        self.height = 0
        self.width = 0
        self.message = 'test'
        self.messageTime = time.time()
        self.setScreen(screen)
        self.location = expanduser("~")
        self.selection = []
        self.index = []
        self.folderList = []
        self.loadFolder(self.location)
    def enter(self):
        self.clear()
    def leave(self):
        pass
    def draw(self):
        self.clear()
        self.screen.addstr(0, 0, 'Folder')
        i = 1
        for e in self.folderList:
            if i == self.height - 1:
                break
            self.screen.addstr(i, 0, e['name'])
            i += 1
        self.showMessage()
        self.refresh()

    def loadFolder(self, path)
        self.folderList = []
        elements = os.listdir(path)
        for e in elements:
            entry = {'name': e}
            self.folderList.append(entry)

    def handleInput(self, key):
        self.setMessage(key)
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
        return ''
    def showMessage(self):
        if self.isMessage():
            self.screen.addstr(self.height - 1, 0, self.message)
    def isMessage(self):
        if self.message != '':
            if time.time() - self.messageTime > 1:
                self.resetMessage()
        return self.message != ''
    def resetMessage(self):
        self.message = ''
    def setMessage(self, message):
        self.message = message
        self.messageTime = time.time()

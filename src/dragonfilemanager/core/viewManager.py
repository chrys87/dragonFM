import sys,os
import curses

from dragonfilemanager.core import mainMenuManager
from dragonfilemanager.core import tabManager

class viewManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.commandManager = self.dragonfmManager.getCommandManager()
        self.tabs = {}
        self.tabList = []
        self.mainMenuManager = mainMenuManager.mainMenuManager(self.dragonfmManager)
        self.currentID = -1
        self.mode = 0 # 0: folder, 1: context menu
        self.addTab()
        self.addTab()
        self.addTab()
        self.addTab()
        self.addTab()
    def getNewID(self):
        for i in range(1000):
            if not i in self.tabList:
                return i
        return None
    def addTab(self, changeToNew = True, newID = None):
        if self.mode != 0:
            return False
        id = None
        if newID == None:
            id = self.getNewID()
        else:
            id = newID
        if id == None:
            return False
        self.tabs[id] = tabManager.tabManager(id, self.dragonfmManager)
        if self.tabList == []:
            self.tabList = [id]
        else:
            self.tabList = self.tabList[:self.getCurrentIndex() + 1] + [id] + self.tabList[self.getCurrentIndex() + 2:]
        if changeToNew:
            self.changeTab(id)
        return True
    def closeCurrentTab(self):
        self.closeTab(self.currentID)
    def closeTab(self, id):
        if self.mode != 0:
            return
        if len(self.tabs) > 1:
            tabIndex = -1
            try:
                tabIndex = self.tabList.index(id)
                self.tabList.remove(id)
                if tabIndex >= len(self.tabList):
                    tabIndex = len(self.tabList) - 1
                newID = self.tabList[tabIndex]
                self.changeTab(newID)
                del(self.tabs[id])
            except:
                pass
        else:
            self.dragonfmManager.stop()
    def getCurrentIndex(self):
        return self.getIndexForID(self.currentID)
    def getIndexForID(self, id):
        return self.tabList.index(id)
    def changeMode(self, mode):
        if self.mode == mode:
            return
        if self.mode == 0:
            self.tabs[self.getCurrentIndex()].leave()
        elif self.mode == 1:
            self.mainMenuManager.leave()

        if mode == 0:
            self.tabs[self.getCurrentIndex()].enter()
        elif mode == 1:
            self.mainMenuManager.enter()
        self.mode = mode
    def prevTab(self):
        currIndex = self.getCurrentIndex()
        currIndex -= 1
        if currIndex < 0:
            currIndex = len(self.tabList) - 1
        self.changeTab(self.tabList[currIndex])
    def nextTab(self):
        currIndex = self.getCurrentIndex()
        currIndex += 1
        if currIndex >= len(self.tabList):
            currIndex = 0
        self.changeTab(self.tabList[currIndex])
    def changeTab(self, id):
        if self.mode != 0:
            return
        # old
        if self.currentID != -1:
            if self.tabList[self.getCurrentIndex()] == id:
                return
            self.tabs[self.getCurrentIndex()].leave()
        # new
        self.tabs[self.getIndexForID(id)].enter()
        self.currentID = id
    def getCurrentTab(self):
        return self.getTab(self, self.getCurrentIndex())
    def getTab(self, id):
        return self.tabs[id]
    def update(self):
        if self.mode == 0:
            self.tabs[self.getCurrentIndex()].update()
        elif self.mode == 1:
            self.mainMenuManager.update()
        self.screen.addstr(8, 0, str(self.tabList))

    def handleVeiwInput(self, shortcut):
        command = self.settingsManager.getShortcut('view-keyboard', shortcut)
        if command == '':
            return False
        return self.commandManager.runCommand('view', command)
    def handleInput(self, shortcut):
        if not self.handleVeiwInput(shortcut):
            if self.mode == 0:
                self.tabs[self.getCurrentIndex()].handleInput(shortcut)
            elif self.mode == 1:
                self.mainMenuManager.handleInput(shortcut)

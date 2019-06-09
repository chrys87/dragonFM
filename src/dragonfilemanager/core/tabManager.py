import sys, os, curses

from dragonfilemanager.core import detailManager
from dragonfilemanager.core import listManager

class tabManager():
    def __init__(self, id, dragonfmManager):
        self.id = id
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.listManager = listManager.listManager(self.id, self.dragonfmManager)        
        self.detailManager = detailManager.detailManager(self.id, self.dragonfmManager)
        self.commandManager = self.dragonfmManager.getCommandManager()
        self.mode = 0 # 0: folder, 1: details
    def enter(self):
        self.update()
    def leave(self):
        pass
    def changeMode(self, mode):
        if self.mode == mode:
            return
        if self.mode == 0:
            self.listManager.leave()
        elif self.mode == 1:
            self.detailManager.leave()

        if mode == 0:
            self.listManager.enter()
        elif mode == 1:
            self.detailManager.enter()

        self.mode = mode
    def update(self):
        if self.mode == 0:
            self.listManager.update()
        elif self.mode == 1:
            self.detailManager.update()
    def handleTabInput(self, shortcut):
        command = self.settingsManager.getShortcut('tab-keyboard', shortcut)
        if command == '':
            return False
        if not self.commandManager.isCommandActive('tab', command):
            return False
        return self.commandManager.runCommand('tab', command)
    def handleInput(self, shortcut):
        if not self.handleTabInput(shortcut):
            if self.mode == 0:
                self.listManager.handleInput(shortcut)
            elif self.mode == 1:
                self.detailManager.handleInput(shortcut)
    def getListManager(self):
        return self.listManager
    def getDetailManager(self):
        return self.detailManager
    def __del__(self):
        # stop watchdog
        try:
            self.getListManager().shutdown()
            self.getDetailManager().shutdown()
        except:
            pass

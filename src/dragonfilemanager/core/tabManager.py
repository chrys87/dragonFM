import sys,os
import curses

from dragonfilemanager.core import contextMenuManager
from dragonfilemanager.core import folderManager

class tabManager():
    def __init__(self, id, dragonfmManager):
        self.id = id
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.folderManager = folderManager.folderManager(self.id, self.dragonfmManager)        
        self.contextMenuManager = contextMenuManager.contextMenuManager(self.id, self.dragonfmManager)
        self.mode = 0 # 0: folder, 1: context menu
    def enter(self):
        self.update()
    def leave(self):
        pass
    def changeMode(self, mode):
        if self.mode == mode:
            return
        if self.mode == 0:
            self.folderManager.leave()
        elif self.mode == 1:
            self.contextMenuManager.leave()

        if mode == 0:
            self.folderManager.enter()
        elif mode == 1:
            self.contextMenuManager.enter()

        self.mode = mode

    def update(self):
        if self.mode == 0:
            self.folderManager.update()
        elif self.mode == 1:
            self.contextMenuManager.update()
    def handleTabInput(self, shortcut):
        command = self.settingsManager.getShortcut('tab-keyboard', shortcut)
        if command == '':
            return False
        return self.commandManager.runCommand('tab', command)
    def handleInput(self, shortcut):
        if not self.handleTabInput(shortcut):
            if self.mode == 0:
                self.folderManager.handleInput(shortcut)
            elif self.mode == 1:
                self.contextMenuManager.handleInput(shortcut)

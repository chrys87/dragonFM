import sys,os
import curses

from dragonfilemanager.core import mainMenuManager
from dragonfilemanager.core import tabManager

class viewManager():
    def __init__(self, dragonfmManager):
        self.mode = 0 # 0: tab, 1: Main Menu
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.tabManager = tabManager.tabManager(self.dragonfmManager)
        self.mainMenuManager = mainMenuManager.mainMenuManager(self.dragonfmManager)

    def changeMode(self, mode):
        if self.mode == mode:
            return
        if self.mode == 0:
            self.tabManager.leave()
        elif self.mode == 1:
            self.mainMenuManager.leave()

        if mode == 0:
            self.tabManager.enter()
        elif mode == 1:
            self.mainMenuManager.enter()
        self.mode = mode

    def update(self):
        if self.mode == 0:
            self.tabManager.draw()
        elif self.mode == 1:
            self.mainMenuManager.draw()
    def handleViewInput(self, key):
        return False
    def handleInput(self, key):
        if not self.handleViewInput(key):
            if self.mode == 0:
                self.tabManager.handleInput(key)
            elif self.mode == 1:
                self.mainMenuManager.handleInput(key)

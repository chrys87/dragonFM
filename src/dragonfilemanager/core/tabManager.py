import sys,os
import curses

from dragonfilemanager.core import mainMenuManager
from dragonfilemanager.core import folderManager

class tabManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.tabs = {}
        self.mainMenu = mainMenuManager.mainMenuManager(self.dragonfmManager)
        self.currentTab = -1
        self.mode = 0 # 0: folder, 1: context menu
        self.addTab()
    def addTab(self, changeToNew = True):
        if self.mode != 0:
            return
        id = len(self.tabs)
        self.tabs[id] = folderManager.folderManager(id, self.dragonfmManager)
        if changeToNew:
            self.changeTab(id)

    def closeTab(self, tab):
        if self.mode != 0:
            return
        if len(self.tabs) > 1:
            if tab == self.currentTab:
                self.changeTab(0)
            del(self.tabs[tab])
    def changeMode(self, mode):
        if self.mode == mode:
            return
        if self.mode == 0:
            self.tabs[self.currentTab].leave()
        elif self.mode == 1:
            self.mainMenu.leave()

        if mode == 0:
            self.tabs[self.currentTab].enter()
        elif mode == 1:
            self.mainMenu.enter()

        self.mode = mode

    def changeTab(self, currentTab):
        if self.mode != 0:
            return
        if self.currentTab == currentTab:
            return
        if currentTab < 0:
            currentTab = len(self.tabs) - 1
        if currentTab >= len(self.tabs):
            currentTab = 0
        # old
        if self.currentTab != -1:
            self.tabs[self.currentTab].leave()
        # new
        self.tabs[currentTab].enter()
        self.currentTab = currentTab

    def update(self):
        if self.mode == 0:
            self.tabs[self.currentTab].draw()
        elif self.mode == 1:
            self.mainMenu.draw()

    def handleInput(self, key):
        if self.mode == 0:
            self.tabs[self.currentTab].handleInput(key)
        elif self.mode == 1:
            self.mainMenu.handleInput(key)

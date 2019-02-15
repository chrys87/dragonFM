import sys,os
import curses

from dragonfilemanager.core import menuManager
from dragonfilemanager.core import folderManager

class viewManager():
    def __init__(self):
        self.tabs = [folderManager.folderManager()]
        self.menu = menuManager.menuManager()
        self.currentTab = 0
        self.mode = 0 # 0: folder, 1: menu
    def update(self):
        if self.mode == 0:
            self.tabs[self.currentTab].drawWrapper()
        elif self.mode == 1:
            self.menu.drawWrapper()
    def handleInput(self, key):
        if self.mode == 0:
            self.tabs[self.currentTab].handleInput(key)
        elif self.mode == 1:
            self.menu.handleInput(key)
    def getScreen(self):
        if self.mode == 0:
            return self.tabs[self.currentTab].getScreen(key)
        elif self.mode == 1:
            return self.menu.getScreen(key)

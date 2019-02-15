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
            self.tabs[self.currentTab].draw()
        elif self.mode == 1:
            self.menu.draw()

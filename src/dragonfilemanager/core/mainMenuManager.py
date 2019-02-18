import sys,os
import curses

class mainMenuManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def enter(self):
        self.screen.clear()
    def leave(self):
        pass
    def draw(self):
        self.screen.addstr(0, 0, 'Menu')
    def handleInput(self, key):
        return False


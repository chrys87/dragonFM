import sys, os
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
    def update(self):
        self.screen.addstr(0, 0, 'Menu')
    def handleMainInput(self, shortcut):
        command = self.settingsManager.getShortcut('main-keyboard', shortcut)
        if command == '':
            return False
        return self.commandManager.runCommand('main', command)
    def handleInput(self, shortcut):
        return self.handleMainInput(shortcut)

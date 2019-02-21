import sys, os, time, inspect, curses

currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
dragonFmPath = os.path.dirname(currentdir)

class contextMenuManager():
    def __init__(self, id, dragonfmManager):
        self.id = id
        self.dragonfmManager = dragonfmManager
        self.screen = dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def enter(self):
        self.clear()
        self.screen.refresh()
        self.update()
    def leave(self):
        pass
    def update(self):
        self.screen.addstr(0, 0, 'Menu')
    def handleContextInput(self, shortcut):
        command = self.settingsManager.getShortcut('context-keyboard', shortcut)
        if command == '':
            return False
        return False
    def handleInput(self, shortcut):
        return self.handleContextInput(shortcut)


import sys, os, time, inspect, curses

currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
dragonFmPath = os.path.dirname(currentdir)

class contextMenuManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def enter(self):
        self.clear()
        self.screen.refresh()
    def leave(self):
        pass
    def draw(self):
        self.screen.addstr(0, 0, 'Menu')
    def handleInput(self, key):
        return False


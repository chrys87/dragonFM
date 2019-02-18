import sys,os
import curses

class inputManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def get(self):
        if not self.screen:
            return None
        return self.screen.getkey()

import sys, os, curses

class clipboardManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.clipboard = {}
    def setClipboard(self, selection):
        if selection == None:
            return 
        self.clipboard = selection.copy()
    def clearClipboard(self):
        self.clipboard = {}
    def getClipboard(self):
        return self.clipboard.copy()
        

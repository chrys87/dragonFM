import sys, os, curses

class clipboardManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.clipboard = {}
    def setClipboard(self, selection):
        if selection == None:
            self.clearClipboard()
        if selection == {}:
            self.clearClipboard()            
        self.clipboard = selection.copy()
    def clearClipboard(self):
        self.clipboard = {}
        

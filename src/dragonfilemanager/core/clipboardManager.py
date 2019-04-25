import sys, os, curses

class clipboardManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.clipboard = []
        self.operation = '' # copy, cut
    def setClipboard(self, selection, operation = 'copy'):
        if selection == None:
            return 
        self.clipboard = selection.copy()
        self.operation = operation
    def clearClipboard(self):
        self.clipboard = []
        self.operation = ''
    def getClipboard(self):
        return self.clipboard.copy()
    def getOperation(self):
        return self.operation
    def isClipboardEmpty(self):
        return self.getClipboard() == []

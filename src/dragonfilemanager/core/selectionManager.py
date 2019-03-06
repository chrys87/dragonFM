import sys, os, curses

class selectionManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.viewManager = self.dragonfmManager.getViewManager()
        
    def getSelectionCurrentTab(self):
        return None
    def getCursorCurrentTab(self):
        return None
    

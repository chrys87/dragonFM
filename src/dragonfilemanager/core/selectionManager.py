import sys, os, curses

class selectionManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.viewManager = self.dragonfmManager.getViewManager()
        
    def getSelectionCurrentTab(self):
        return [].copy()
    def getCursorCurrentTab(self):
        return None
    def getSelectionOrCursorCurrentTab(self):
        # use active cursor if no selection is done.
        # return list of file elements or None if no elements exists
        currentSelection = None
        selection = self.getSelectionCurrentTab()
        if selection == []:
            currentCursor = self.getCursorCurrentTab()
            if currentCursor != None:
                currentSelection = [currentCursor]
        else:
            currentSelection = selection
        return currentSelection 

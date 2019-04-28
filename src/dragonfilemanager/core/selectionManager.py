import sys, os, curses

class selectionManager():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def getSelectionCurrentTab(self):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        return folderManager.getSelection()
    def getCursorCurrentTab(self):
        folderManager = self.dragonfmManager.getCurrFolderManager() 
        return folderManager.getCurrentKey()
    def getSelectionOrCursorCurrentTab(self):
        #return [self.getCursorCurrentTab()]
        # use active cursor if no selection is done.
        # return list of file elements or None if no elements exists
        currentSelection = []
        currentCursor = None
        selection = self.getSelectionCurrentTab()
        if selection == []:
            currentCursor = self.getCursorCurrentTab()
            if currentCursor != None:
                currentSelection = [currentCursor]
        else:
            currentSelection = selection
        return currentSelection

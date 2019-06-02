#!/usr/bin/env python
import os
class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Rename')
    def getDescription(self):
        return _('Rename a file or folder')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()
        currentCursor = self.selectionManager.getCursorCurrentTab()
        if currentCursor == None:
            return
        if not os.path.exists(currentCursor):
            return
        currEntryName = os.path.basename(currentCursor)
        inputDialog = self.dragonfmManager.createInputDialog(description = ['Please enter a new name:'], initValue = currEntryName)
        exitStatus, newEntryName = inputDialog.show()
        if not exitStatus:
            return
        if currEntryName == newEntryName:
            return
        if not location.endswith('/'):
            location += '/'
        fullPath = '{0}{1}'.format(location, newEntryName)
        self.fileManager.moveEntry(currentCursor, fullPath)
        if callback:
            callback()

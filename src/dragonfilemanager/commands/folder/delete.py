#!/usr/bin/env python

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Delete')
    def getDescription(self):
        return _('Delete current entry or selection')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        folderManager = self.dragonfmManager.getCurrFolderManager()

        # Get the files and directories that were selected.
        selection = self.selectionManager.getSelectionOrCursorCurrentTab()

        self.fileManager.spawnDeleteSelectionThread(selection)
        if folderManager.getSelectionMode() != 0:
            folderManager.setSelectionMode(0)

        if callback:
            callback()

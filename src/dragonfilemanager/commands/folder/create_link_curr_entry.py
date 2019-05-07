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
        return _('Create Link')
    def getDescription(self):
        return _('Create a link of the current entry')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        folderManager = self.dragonfmManager.getCurrFolderManager()
        
        # Get the files and directories that were selected.
        currentCursor = self.selectionManager.getCursorCurrentTab()
        if currentCursor == None:
            return
        if not os.path.exists(currentCursor):
            return
        filename_w_ext = os.path.basename(currentCursor)
        fileName, fileExtension = os.path.splitext(filename_w_ext)
        
        location = folderManager.getLocation()
        linkName = self.fileManager.getInitName(location, '{0}-{1}{2}.link', fileName)
     
        fullPath = '{0}/{1}'.format(location, linkName)        
        self.fileManager.spawnCreateLinkCursorThread(currentCursor, fullPath)
        if callback:
            callback()

#!/usr/bin/env python

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Create Folder')
    def getDescription(self):
        return _('Create a new folder')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        folderManager = self.dragonfmManager.getCurrFolderManager()        
        location = folderManager.getLocation()
        fullPath = location + 'newFolder'        
        self.fileManager.spawnCreateFolderThread(fullPath)
        if callback:
            callback()

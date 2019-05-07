#!/usr/bin/env python

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Create File')
    def getDescription(self):
        return _('Create a new file')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        folderManager = self.dragonfmManager.getCurrFolderManager()
        location = folderManager.getLocation()
        fileName = self.fileManager.getInitName(location, 'new_file{0}{1}{2}.txt', '_')
        fullPath = '{0}/{1}'.format(location, fileName)
        self.fileManager.spawnCreateFileThread(fullPath)
        if callback:
            callback()

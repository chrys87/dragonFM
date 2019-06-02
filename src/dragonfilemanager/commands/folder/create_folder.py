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
        folderName = self.fileManager.getInitName(location, 'new_folder{0}{1}{2}', '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Foldername:'])
        inputDialog.setDefaultValue(folderName)

        exitStatus, folderName = inputDialog.show()
        if not exitStatus:
            return

        if not location.endswith('/'):
            location += '/'
        fullPath = '{0}{1}'.format(location, folderName)
        self.fileManager.spawnCreateFolderThread(fullPath)
        if callback:
            callback()

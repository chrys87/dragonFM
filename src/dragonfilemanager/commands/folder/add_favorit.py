#!/usr/bin/env python
import os
from os.path import expanduser

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
        return _('Create a link to the current entry')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        folderManager = self.dragonfmManager.getCurrFolderManager()
        location = folderManager.getLocation()

        if not os.path.exists(location):
            return

        favoritName = os.path.basename(location)

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Favoritname:'], initValue = favoritName)
        exitStatus, favoritName = inputDialog.show()
        if not exitStatus:
            return
        favDir = expanduser(self.settingsManager.get('favorits', 'path'))
        if not os.path.exists(favDir):
            os.makedirs(favDir)

        if not favDir.endswith('/'):
            favDir += '/'
        if not location.endswith('/'):
            location += '/'

        destPath = '{0}{1}'.format(favDir, favoritName)

        self.fileManager.spawnCreateLinkCursorThread(location, destPath)
        if callback:
            callback()

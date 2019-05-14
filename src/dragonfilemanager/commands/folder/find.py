#!/usr/bin/env python
import os

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Search')
    def getDescription(self):
        return _('Search for file or folder')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        folderManager = self.dragonfmManager.getCurrFolderManager()
        location = folderManager.getLocation()

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Find:'], initValue = '')
        exitStatus, searchString = inputDialog.show()
        if not exitStatus:
            return
        collectorParam = {'search':searchString}
        folderManager.setCollector(self.findCollector, collectorParam)

        folderManager.setRequestReload()

        if callback:
            callback()

    def findCollector(self, collectorParam):
        path = collectorParam['path']
        searchString = collectorParam['search']

        entries = {}

        for root, dirs, files in os.walk(path):
            for fn in files:
                if fn.startswith('.'):
                    if not self.settingsManager.getBool('folder', 'showHidden'):
                        continue
                if fn.endswith(searchString):
                    fullPath = os.path.join(root, fn)
                    entry = self.fileManager.getInfo(fullPath)
                    if entry != None:
                        entries[fullPath] = entry
        return entries

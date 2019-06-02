#!/usr/bin/env python
import os
from os.path import expanduser

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

        folderManager.setColumns(self.settingsManager.get('favorits', 'columns'))
        favDir = expanduser(self.settingsManager.get('favorits', 'path'))
        collectorParam = {'favPath':favDir}
        folderManager.setCollector(self.favCollector, collectorParam)

        folderManager.setRequestReload()

        if callback:
            callback()

    def favCollector(self, collectorParam):
        favDir = collectorParam['favPath']
        elements = os.listdir(favDir)
        entries = {}
        for e in elements:
            fullPath = favDir
            if not fullPath.endswith('/'):
                fullPath += '/'
            fullPath += e
            entry = self.fileManager.getInfo(fullPath)
            if entry != None:
                entries[fullPath] = entry
        return entries, favDir

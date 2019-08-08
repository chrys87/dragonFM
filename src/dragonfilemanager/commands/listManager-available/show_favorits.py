from dragonfilemanager.core.baseCommand import baseCommand
import os
from os.path import expanduser

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.setname('Search')
        self.setDescription('Search for file or folder')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()
        location = listManager.getLocation()

        listManager.setColumns(self.settingsManager.get('favorits', 'columns'))
        favDir = expanduser(self.settingsManager.get('favorits', 'path'))
        collectorParam = {'favPath':favDir}
        listManager.setCollector(self.favCollector, collectorParam)

        listManager.setRequestReload()

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

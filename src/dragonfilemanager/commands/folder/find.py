#!/usr/bin/env python
import os, re, fnmatch

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
        folderManager.setCollector(self.findCollector, collectorParam)
        folderManager.setColumns(self.settingsManager.get('search', 'columns'))
        folderManager.setRequestReload()

        if callback:
            callback()

    def findCollector(self, collectorParam):
        path = collectorParam['path']
        searchString = collectorParam['search']
        showHidden = self.settingsManager.getBool('folder', 'showHidden')
        entries = {}
        for root, dirs, files in os.walk(path):
            allElements = dirs + files
            for e in allElements:
                if not showHidden:
                    if e.startswith('.'):
                        continue
                globFound = False
                regextFound = False
                foundInString = False
                found = False
                # search exact name in string
                if not found:
                    if searchString in e:
                        foundInString = True
                        found = foundInString or found
                # search glob
                if not found:
                    try:
                        globFound = fnmatch.fnmatch(e, searchString)
                        found = globFound or found
                    except:
                        pass
                # search regex
                if not found:
                    try:
                        regextFound = re.search(searchString, e)
                        found = regextFound or found
                    except:
                        pass
                # add entry if it was match
                if found:
                    fullPath = os.path.join(root, e)
                    entry = None
                    try:
                        entry = self.fileManager.getInfo(fullPath)
                    except:
                        pass
                    if entry != None:
                        entries[fullPath] = entry
        return entries, collectorParam['path']

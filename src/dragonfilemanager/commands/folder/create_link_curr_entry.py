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
        return _('Create a link to the current entry')
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
        nameTemplate = fileName + '_link{0}{1}{2}'

        if fileExtension != None:
            if fileExtension != '':
                nameTemplate += fileExtension

        linkName = self.fileManager.getInitName(location, nameTemplate, '_')

        inputDialog = self.dragonfmManager.createInputDialog(description = ['Linkname:'], initValue = linkName)
        exitStatus, linkName = inputDialog.show()
        if not exitStatus:
            return

        if not location.endswith('/'):
            location += '/'
        fullPath = '{0}{1}'.format(location, linkName)

        self.fileManager.spawnCreateLinkCursorThread(currentCursor, fullPath)
        if callback:
            callback()

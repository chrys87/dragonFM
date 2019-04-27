#!/usr/bin/env python

import os, shutil

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('No description found')
    def getDescription(self):
        return _('No description found')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        folderManager = self.dragonfmManager.getCurrFolderManager()
        
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
                                                                                                                                                                
        # Loop through the files and directories and delete them.
        for i in selected:
            if os.is_file(i):
                os.remove(i)
            if os.is_dir(i):
                shutil.rmtree(i)
        folderManager.setNeedRefresh()
        if callback:
            callback()

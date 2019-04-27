#!/usr/bin/env python

import os, shutil

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
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
        for path in selected:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                pass
            
        folderManager.reloadFolder()
        if callback:
            callback()

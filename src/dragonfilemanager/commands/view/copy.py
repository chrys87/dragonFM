#!/usr/bin/env python

import shutil

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.folderManager = self.dragonfmManager.getFolderManager()
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
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
                                                                                                                                                                
        # Loop through the files and directories and copy them.
        for i in selected:
            try:
                shutil.copy2(i, self.folderManager.getLocation())
            except:
                pass
        if callback:
            callback()

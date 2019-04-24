#!/usr/bin/env python

import shutil

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.viewManager = None        
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
        if self.viewManager == None:
            self.viewManager = self.dragonfmManager.getViewManager()
        folderManager = self.viewManager.getCurrentTab().getFolderManager()

        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
                                                                                                                                                                
        # Loop through the files and directories and move them to the selected destination.
        for i in selected:
            try:
                shutil.move(i, folderManager.getLocation())
            except:
                pass
        if callback:
            callback()

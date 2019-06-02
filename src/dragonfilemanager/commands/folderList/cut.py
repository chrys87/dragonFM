#!/usr/bin/env python

import shutil

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.clipboardManager = self.dragonfmManager.getClipboardManager()        
    def shutdown(self):
        pass
    def getName(self):
        return _('Cut')
    def getDescription(self):
        return _('Cut current entry or selection')
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

        self.clipboardManager.setClipboard(selected, operation = 'cut')
        if folderManager.getSelectionMode() != 0:
            folderManager.setSelectionMode(0)

        if callback:
            callback()

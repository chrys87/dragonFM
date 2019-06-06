#!/usr/bin/env python

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Delete')
    def getDescription(self):
        return _('Delete current entry or selection')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):   
        listManager = self.dragonfmManager.getCurrListManager()

        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()

        inputDialog = self.dragonfmManager.createInputDialog(description = [_('Do you realy want to delete {} elements:').format(len(selected))])
        inputDialog.setDefaultValue('n')
        inputDialog.setConfirmationMode(True)
        exitStatus, answer = inputDialog.show()
        if not exitStatus:
            return
        if answer == 'n':
            return
        self.fileManager.spawnDeleteSelectionThread(selected)
        if listManager.getSelectionMode() != 0:
            listManager.setSelectionMode(0)

        if callback:
            callback()

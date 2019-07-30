#!/usr/bin/env python

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.processManager = self.dragonfmManager.getProcessManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Email')
    def getDescription(self):
        return _('Send selected files as email attachements.')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)
        if countSelected == 0:
            self.dragonfmManager.setMessage('No files selected for mailing')
            return

        fileParameter = self.processManager.convertListToString(selected)
        cmd = self.settingsManager.get('application', 'sendmail')
        cmd = cmd.format(fileParameter)
        self.processManager.startExternal(cmd)

        if callback:
            callback()

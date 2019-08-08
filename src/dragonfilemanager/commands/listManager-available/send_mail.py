from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.processManager = self.dragonfmManager.getProcessManager()
        self.setName('Email')
        self.setDescription('Send selected files as e-mail attachments.')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1)
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

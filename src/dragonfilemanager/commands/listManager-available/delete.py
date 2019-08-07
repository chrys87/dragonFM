from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.fileManager = self.dragonfmManager.getFileManager()
        self.setName('Delete')
        self.setDescription('Delete current entry or selection')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1)
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

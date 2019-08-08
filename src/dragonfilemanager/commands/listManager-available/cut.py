from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.clipboardManager = self.dragonfmManager.getClipboardManager()
        self.setName('Cut')
        self.setDescription('Cut current entry or selection')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1)
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()

        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)
        self.clipboardManager.setClipboard(selected, operation = 'cut')
        if listManager.getSelectionMode() != 0:
            listManager.setSelectionMode(0)
        self.dragonfmManager.setMessage('cut {0} elements'.format(countSelected))

        if callback:
            callback()

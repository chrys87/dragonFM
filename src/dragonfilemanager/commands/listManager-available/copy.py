from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.setName('Copy')
        self.setDescription('Copy current entry or selection')
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
        self.clipboardManager = self.dragonfmManager.getClipboardManager()
    def active(self):
        return self.commandManager.isCommandValidForFileOperation(minSelection = 1)
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()

        # Get the files and directories that were selected.
        selected = self.selectionManager.getSelectionOrCursorCurrentTab()
        countSelected = len(selected)

        self.clipboardManager.setClipboard(selected)
        if listManager.getSelectionMode() != 0:
            listManager.setSelectionMode(0)
        self.dragonfmManager.setMessage('copy {0} elements'.format(countSelected))

        if callback:
            callback()

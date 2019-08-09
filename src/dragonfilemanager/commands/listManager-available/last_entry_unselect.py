from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Last Entry')
        self.setDescription('Move cursor to last entry')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.lastEntry()
        listManager.unselectAllEntries()
        if callback:
            callback()

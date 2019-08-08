from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Previous Entry')
        self.setDescription('Move Cursor to previous entry')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.selectCurrentEntry()
        listManager.prevEntry()
        listManager.selectCurrentEntry()
        if callback:
            callback()

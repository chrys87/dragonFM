from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName _('Leave entry')
        self.setDescription('Go to parent')
    def active(self):
        return self.commandManager.isCommandValidForFileOperation()
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.parentEntry()
        if callback:
            callback()

from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('First Entry')
        self.setDescription('Move cursor to first entry and keep selection')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.firstEntry()
        if callback:
            callback()

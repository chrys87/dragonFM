from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.setName('Activate Entry')
        self.setDescription('Activate current entry')
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def run(self, callback = None):
        detailManager = self.dragonfmManager.getCurrDetailManager()
        detailManager.activateCurrentEntry()
        if callback:
            callback()

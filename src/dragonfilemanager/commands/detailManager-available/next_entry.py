from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.setName('Next Entry')
        self.setDescription('Move Cursor to next entry')
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def run(self, callback = None):
        detailManager = self.dragonfmManager.getCurrDetailManager()
        detailManager.nextEntry()
        if callback:
            callback()

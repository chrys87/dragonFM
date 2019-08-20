from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Select All')
        self.setDescription('Select All entries in the current folder')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.selectAllEntries()
        if callback:
            callback()

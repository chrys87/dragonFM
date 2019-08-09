from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Toggle Selection Mode')
        self.setDescription('Toggles Selection Mode')
     def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.nextSelectionMode()
        if callback:
            callback()

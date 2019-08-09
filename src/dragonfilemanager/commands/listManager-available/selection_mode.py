from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Selection Mode')
        self.setDescription('Select on navigation')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.setSelectionMode(1)
        listManager.selectCurrentEntry()
        if callback:
            callback()

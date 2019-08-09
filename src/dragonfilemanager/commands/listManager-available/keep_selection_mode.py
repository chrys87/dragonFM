from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Keep Selection Mode')
        self.setDescription('Keep Selection while navigating')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.setSelectionMode(2)
        if callback:
            callback()

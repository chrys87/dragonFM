from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.setName('Previous Page')
        self.setDescription('Goto previous Page')
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.prevPage()
        if callback:
            callback()

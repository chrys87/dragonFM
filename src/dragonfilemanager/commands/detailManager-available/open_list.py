from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.setName('Open List')
        self.setDescription('Opens the List')
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def run(self, callback = None):
        tabManager = self.dragonfmManager.getViewManager().getCurrentTab()
        tabManager.changeMode(0) # list
        if callback:
            callback()

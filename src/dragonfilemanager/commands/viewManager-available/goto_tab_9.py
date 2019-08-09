from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.setName('Goto Tab 9')
        self.setDescription('Change to tab 9')
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.viewManager = None
    def run(self, callback = None):
        if self.viewManager == None:
            self.viewManager = self.dragonfmManager.getViewManager()
        self.viewManager.changeTabIndex(9)
        if callback:
            callback()

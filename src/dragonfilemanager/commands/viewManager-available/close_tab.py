from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.setName('Close Tab')
        self.setDescription('Close the current tab')
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.viewManager = None
    def run(self, callback = None):
        if self.viewManager == None:
            self.viewManager = self.dragonfmManager.getViewManager()
        self.viewManager.closeCurrentTab()
        if callback:
            callback()

from dragonfilemanager.core.baseCommand import baseCommand

class command(baseCommand):
    def __init__(self, dragonfmManager):
        baseCommand.__init__(self, dragonfmManager)
        self.setName('Display Help')
        self.setDescription('Documentation for the Dragon File Manager.')
        self.screen = self.dragonfmManager.getScreen()
        self.processManager = self.dragonfmManager.getProcessManager()
    def getShortcut(self):
        return "F1"
    def run(self, callback = None):
        self.processManager.startExternal('man bash')
        if callback:
            callback()

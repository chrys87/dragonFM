class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.processManager = self.dragonfmManager.getProcessManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Display Help')
    def getDescription(self):
        return _('Documentation for the Dragon File Manager.')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return "F1"
    def run(self, callback = None):
        self.processManager.startExternal('man bash')
        if callback:
            callback()

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Toggle Selection Mode')
    def getDescription(self):
        return _('Toggles Selection Mode')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        folderManager.nextSelectionMode()
        if callback:
            callback()

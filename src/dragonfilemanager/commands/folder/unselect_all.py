class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Unselect All')
    def getDescription(self):
        return _('Unselect all entries')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        if folderManager.unselectAllEntries():
            folderManager.setRequestUpdate()
        if callback:
            callback()

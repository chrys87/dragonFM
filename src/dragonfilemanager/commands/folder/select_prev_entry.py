class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Previous Entry')
    def getDescription(self):
        return _('Move Cursor to previous entry')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        if folderManager.selectCurrentEntry():
            folderManager.setRequestUpdate()
        folderManager.prevEntry()
        if folderManager.selectCurrentEntry():
            folderManager.setRequestUpdate()
        if callback:
            callback()

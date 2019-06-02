class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('toggle selection / unselection')
    def getDescription(self):
        return _('toggle selection / unselection on navigation')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        if folderManager.getSelectionMode() == 0:
            folderManager.setSelectionMode(1)
            folderManager.selectCurrentEntry()
        else:
            folderManager.setSelectionMode(0)
            folderManager.unselectAllEntries()
        if callback:
            callback()

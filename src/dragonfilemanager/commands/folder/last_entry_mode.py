class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Last Entry use mode')
    def getDescription(self):
        return _('Move cursor to last entry using current mode')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        folderManager.lastEntry()
        # unselection mode
        if folderManager.getSelectionMode() == 0:
            folderManager.unselectAllEntries()
        # selection mode
        elif folderManager.getSelectionMode() == 1:
            folderManager.selectCurrentEntry()
        # ignore mode
        elif folderManager.getSelectionMode() == 2:
            pass
        if callback:
            callback()

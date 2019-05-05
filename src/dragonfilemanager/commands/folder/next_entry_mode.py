class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Next Entry use mode')
    def getDescription(self):
        return _('Move Cursor to next entry using current mode')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        folderManager = self.dragonfmManager.getCurrFolderManager()
        if folderManager.getSelectionMode() == 1:
            if folderManager.selectCurrentEntry():
                folderManager.setNeedRefresh()
        folderManager.nextEntry()
        # unselection mode
        if folderManager.getSelectionMode() == 0:
            if folderManager.unselectAllEntries():
                folderManager.setNeedRefresh()
        # selection mode
        elif folderManager.getSelectionMode() == 1:
            if folderManager.selectCurrentEntry():
                folderManager.setNeedRefresh()        
        # ignore mode
        elif folderManager.getSelectionMode() == 2:
            pass
        if callback:
            callback()

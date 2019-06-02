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
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.lastEntry()
        # unselection mode
        if listManager.getSelectionMode() == 0:
            listManager.unselectAllEntries()
        # selection mode
        elif listManager.getSelectionMode() == 1:
            listManager.selectCurrentEntry()
        # ignore mode
        elif listManager.getSelectionMode() == 2:
            pass
        if callback:
            callback()

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Toggle selection')
    def getDescription(self):
        return _('Select or Unselect the current element')
    def active(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        if listManager.isCurrentEntrySelected():
            listManager.uncselectCurrentEntry()
        else:    
            listManager.selectCurrentEntry()
        if callback:
            callback()

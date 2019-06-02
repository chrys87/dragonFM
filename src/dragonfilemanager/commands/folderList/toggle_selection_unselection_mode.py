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
        listManager = self.dragonfmManager.getCurrListManager()
        if listManager.getSelectionMode() == 0:
            listManager.setSelectionMode(1)
            listManager.selectCurrentEntry()
        else:
            listManager.setSelectionMode(0)
            listManager.unselectAllEntries()
        if callback:
            callback()

class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Reset')
    def getDescription(self):
        return _('Reset All')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        listManager = self.dragonfmManager.getCurrListManager()
        listManager.setSelectionMode(0)
        listManager.resetTypeAheadSearch(True)
        listManager.unselectAllEntries()
        if listManager.getCollectorLocation() != '':
            listManager.setLocation(listManager.getCollectorLocation())
        listManager.setCollector()
        listManager.setRequestReload()
        if callback:
            callback()

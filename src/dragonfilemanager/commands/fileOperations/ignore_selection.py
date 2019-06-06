class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Start Ignore Selection Mode')
    def getDescription(self):
        return _('Keep selection on navigation')
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
        listManager.setSelectionMode(2)
        if callback:
            callback()

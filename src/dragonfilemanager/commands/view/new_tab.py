class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.viewManager = None
    def shutdown(self):
        pass
    def getName(self):
        return _('New Tab')
    def getDescription(self):
        return _('Opens a new Tab')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        if self.viewManager == None:
            self.viewManager = self.dragonfmManager.getViewManager()
        self.viewManager.addTab()
        if callback:
            callback()

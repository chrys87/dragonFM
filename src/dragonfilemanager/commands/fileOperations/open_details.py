class command():
    def __init__(self, dragonfmManager):
        self.dragonfmManager = dragonfmManager
        self.screen = self.dragonfmManager.getScreen()
        self.settingsManager = self.dragonfmManager.getSettingsManager()
        self.selectionManager = self.dragonfmManager.getSelectionManager()
    def shutdown(self):
        pass
    def getName(self):
        return _('Open Details')
    def getDescription(self):
        return _('Opens the Details')
    def active(self):
        return True
    def visible(self):
        return True
    def getValue(self):
        return None
    def getShortcut(self):
        return None
    def run(self, callback = None):
        tabManager = self.dragonfmManager.getViewManager().getCurrentTab()
        detailManager = tabManager.getDetailManager()
        elements = self.selectionManager.getSelectionOrCursorCurrentTab()
        detailManager.setDetails(elements)
        tabManager.changeMode(1) # details
        if callback:
            callback()
